# functional
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision
import wandb
import time

# visualization
import matplotlib.pyplot as plt



def train_epoch(device, train_dataloader, training_params : dict, metrics : dict, log_wandb = True):
    
    # ===== INITIALIZE =====
    # constants
    GENERATOR_LOSS_FUNCTION = training_params["generator_loss_function"]
    GENERATOR_OPTIMIZER = training_params["generator_optimizer"]
    DISCRIMINATOR_LOSS_FUNCTION = training_params["discriminator_loss_function"]
    DISCRIMINATOR_OPTIMIZER = training_params["discriminator_optimizer"]
    BATCH_EVALUATE_EVERY = 1
    LOG_EVERY = training_params["log_every"]
    SAMPLE_SIZE = training_params["sample_size"]
    ALPHA = training_params["alpha"]

    # models
    generator = training_params["generator"].to(device).train()
    discriminator = training_params["discriminator"].to(device).train()

    # epoch metrics
    running_results = {list(metrics.keys())[i] : 0.0 for i in range(len(metrics)) } 
    running_results["loss"] = 0.0
    running_results["loss_discriminator"] = 0.0
    running_results["loss_generator"] = 0.0

    # ===== TRAIN EPOCH =====
    num_batches = 0
    for index, batch in enumerate(train_dataloader, 1):

            # ===== INITIALIZE =====
            num_batches += 1

            # input and ground truth
            input_batched = batch["image"]
            ground_truth_batched = batch["reconstructed"]
            mask_batched = batch["mask"]

            # sanity check
            assert input_batched.shape[0] == ground_truth_batched.shape[0]

            # move tensors to device
            input_batched = input_batched.to(device)
            ground_truth_batched = ground_truth_batched.to(device)
            mask_batched = mask_batched.to(device)

            # Set the gradients to zeros
            GENERATOR_OPTIMIZER.zero_grad()
            DISCRIMINATOR_OPTIMIZER.zero_grad()

            # ===== FORWARD PASS =====
            # 1. reshape to channel first
            input_batched = input_batched.permute(0, 3, 1, 2)
            ground_truth_batched = ground_truth_batched.permute(0, 3, 1, 2)
            mask_batched = mask_batched.permute(0, 3, 1, 2)

            # 2. forward pass by generator to produce images
            input_batched.requires_grad_()
            output_batched = generator(input_batched)

            # 3. splice generated images to that patch is only change
            spliced_batched = ((1-mask_batched) * output_batched) + (mask_batched * ground_truth_batched) 
            
            # 4. generate labels for discriminator
            b, _, _, _ = input_batched.shape
            label_real = torch.ones(b).to(device)
            label_fake = torch.zeros(b).to(device)

            # 5. forward and backward pass on discriminator
            pred_real = discriminator(spliced_batched)
            loss_real = DISCRIMINATOR_LOSS_FUNCTION(pred_real, label_real)
            pred_fake = discriminator(output_batched)
            loss_fake = DISCRIMINATOR_LOSS_FUNCTION(pred_fake, label_fake)
            loss_d = ALPHA * (loss_real + loss_fake)
            loss_d.backward()
            DISCRIMINATOR_OPTIMIZER.step()

            # 6. adverserial and reconstruction loss on generator
            loss_g_reconstruction = GENERATOR_LOSS_FUNCTION(output_batched, ground_truth_batched, mask_batched)
            loss_g_adverserial = loss_fake.item()
            loss_g = loss_g_reconstruction + ALPHA * loss_g_adverserial
            loss_g.backward()
            GENERATOR_OPTIMIZER.step()



            # ===== COMPUTE STATISTICS, USING TORCH METRICS =====  
            # 1. compute losses
            loss = loss_g + loss_d
            running_results["loss"] += loss.detach().item()
            running_results["loss_generator"] += loss_g.detach().item()
            running_results["loss_discriminator"] += loss_d.detach().item()

            # 2. for each key, compute, add item to results dictionary
            for key, func in metrics.items():
                running_results[key] += func(output_batched, ground_truth_batched, mask_batched).detach().item()

            # 3. log with wandb
            if log_wandb and (num_batches % LOG_EVERY == 0):
                batched_predictions = torch.cat([
                    input_batched[:SAMPLE_SIZE, 0:3,:,:], # can be 4 channels
                    ground_truth_batched[:SAMPLE_SIZE,:,:,:],  # 3 channels
                    output_batched[:SAMPLE_SIZE, :,:,:], # 3 channels
                    spliced_batched[:SAMPLE_SIZE,:,:,:]], dim = 0) 
                
                image_array = torchvision.utils.make_grid(batched_predictions, nrow = SAMPLE_SIZE, padding = 50)
                images = wandb.Image(
                    image_array, 
                    caption = "1st row: Damaged, 2nd row: Ground truth, 3rd row: Reconstructed, 4th row: spliced")
                wandb.log( {
                    "images" : images,
                    "loss" : loss.detach().item(),
                    "loss_generator": loss_g.detach().item(),
                    "loss_discriminator" : loss_d.detach().item(),
                    "lr_generator" : GENERATOR_OPTIMIZER.param_groups[0]['lr'],
                    "lr_discriminator" : DISCRIMINATOR_OPTIMIZER.param_groups[0]['lr']

                })
        

            # ===== HOUSEKEEPING =====
            del loss
            del loss_g
            del loss_d
            del input_batched
            del output_batched
            del spliced_batched

            # print results every some batches
            if num_batches % BATCH_EVALUATE_EVERY == 0: 

                args = ""
                for key, val in running_results.items():
                    args += key + ": " + str(running_results[key]/num_batches) + "   "
                print(f"\r{num_batches}/{len(train_dataloader)}: " + args, end = '', flush = True)

    # normalise numbers by batch
    for key, val in running_results.items():
        running_results[key] /= num_batches

    return running_results