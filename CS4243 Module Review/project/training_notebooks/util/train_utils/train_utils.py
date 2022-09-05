# functional
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision
import wandb
import time

# visualization
import matplotlib.pyplot as plt


# ===== VISUALIZATION =====

def sample_batch(dataset, sample_size = 4, show_gray = False):
    """
    This method is intended to help visualize samples from a 
    dataset object. It takes in a dataset and plots out "sample_size"
    number of images from the dataset.
    """

    loader = DataLoader(dataset, batch_size = sample_size, shuffle = True)

    batch = next(iter(loader))
    n = 3
    if show_gray:
        n = 4

    fig, ax = plt.subplots(n, sample_size, figsize = (sample_size * 5, n * 5, ))
    for i in range(sample_size):
        image = batch["image"][i]
        reconstructed = batch["reconstructed"][i]
        mask = batch["mask"][i]
        gray = batch["gray"][i]
        if image.shape[-1] > 3: # take first three channels, rgb
            image = image[:, :, 0:3]

        ax[0][i].imshow(image)
        ax[1][i].imshow(reconstructed)
        ax[2][i].matshow(mask.squeeze())

        if show_gray:
            ax[3][i].matshow(gray)
        
    plt.show()
    plt.close()

def visualize_adj(adj, b: int, h: int, w: int):

    def edge_voting(adj):
        b, hw, hw = adj.shape
        assert hw == h * w
        voted = adj.view(b, hw, h, w).sum(dim = 1)
        return voted
    
    out = edge_voting(adj)
    return out
    

def visualize_results(model, device, running_train_results: dict, running_eval_results: dict, test_dataset = None, images_only = False):
    """
    This method plots the train and validation curves for all defined metrics and loss, and then plots samples of the model
    prediction from the given test dataset. 

    @param model : nn.Module                Model.
    @param device : str                     Device to run predictions on.
    @param running_train_results : dict     Dictionary of lists, key is name, value is list of values over epochs.
    @param running_eval_results : dict      Dictionary of lists, key is name, value is list of values over epochs.
    @param test_dataset : nn.data.Dataset   dataset object to plot samples from.
    @param images_only : bool               boolean flag indicating whether to only plot images and omit training curves.
    """

    # get number of epochs and data points
    NUM_EPOCHS = len(list(running_train_results.values())[0])
    NUM_METRICS = len(list(running_train_results))
    assert list(running_train_results.keys()) == list(running_eval_results.keys())
    
    if not images_only:
        # plot 
        fig, ax = plt.subplots(NUM_METRICS, figsize = (NUM_EPOCHS * 5, NUM_METRICS * 5))
        epochs_axis = [i for i in range(NUM_EPOCHS)]
        index = 0
        for key in list(running_train_results.keys()):
            train = running_train_results[key]
            validation = running_eval_results[key]

            ax[index].plot(epochs_axis, train, label = "train")
            ax[index].plot(epochs_axis, validation, label = "validation")
            ax[index].title.set_text(key)
            index += 1

    if test_dataset != None:
        SAMPLE_SIZE = 8
        loader = DataLoader(test_dataset, batch_size = SAMPLE_SIZE, shuffle = True)
        batch = next(iter(loader))

        # predict
        model.eval()
        output = model(batch["image"].to(device).permute(0, 3, 1, 2)).detach().cpu().permute(0, 2, 3, 1)
        fig, ax = plt.subplots(3, SAMPLE_SIZE, figsize = (SAMPLE_SIZE * 5, 15, ))
        for i in range(SAMPLE_SIZE):
            image = batch["image"][i]
            reconstructed = batch["reconstructed"][i]
            predicted = output[i]

            if image.shape[-1] > 3: 
                image = image[:, :, 0:3] # take rgb if more than 3 channels
                
            ax[0][i].imshow(image)
            ax[1][i].imshow(reconstructed)
            ax[2][i].imshow(predicted)
            
        plt.show()
        plt.close()
    

def summary(model: nn.Module, verbose = False):
    """
    This method helps summarize a model.
    """
    count = 0
    if verbose:
        print(model)

    for name, params in model.named_parameters():
        num_params = params.flatten().size()[0]
        count += num_params
        if verbose:
            print(f"\nlayer: {name}")
            print(f"number of params: {num_params}")
            print(f"params shape: {params.size()}")

    print(f"model has {count/1e6} million parameters")


# ===== TRAINING ===== (templates)

def train_epoch(model, device, train_dataloader, training_params : dict, metrics : dict, log_wandb = True, log_every : int = 1, sample_size : int = 16):
    """
    This method encapsulates the training of a given model for one epoch. 
    
    @param model : nn.Module                        Model to be trained.
    @param device : str                             Device to be trained on.
    @param train_dataloader : nn.data.DataLoader    DataLoader object to load batches of data.
    @param training_params : dict                   Dictionary object mapping names of 
                                                    training utilities to their respective objects.
                                                    Required are "batch_size", "loss_function", 
                                                    and "optimizer". 
    @param metrics : dict                           Dictionary object mapping names of 
                                                    metrics to a functional method that 
                                                    would compute the metric value.
    @param log_wandb : bool
    @param log_every : int
    @param sample_size : int
    """
    
    # ===== INITIALIZE =====
    # constants
    BATCH_SIZE = training_params["batch_size"]
    LOSS_FUNCTION = training_params["loss_function"]
    OPTIMIZER = training_params["optimizer"]
    BATCH_EVALUATE_EVERY = 1
    LOG_EVERY = log_every
    SAMPLE_SIZE = sample_size

    # model to device
    model = model.to(device)
    model.train()

    # epoch metrics
    running_results = {list(metrics.keys())[i] : 0.0 for i in range(len(metrics)) } 
    running_results["loss"] = 0.0

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
            OPTIMIZER.zero_grad()

            # ===== FORWARD PASS =====
            # reshape to channel first
            input_batched = input_batched.permute(0, 3, 1, 2)
            ground_truth_batched = ground_truth_batched.permute(0, 3, 1, 2)
            mask_batched = mask_batched.permute(0, 3, 1, 2)

            # forward pass
            input_batched.requires_grad_()
            output_batched = model(input_batched)

            # ===== BACKPROP =====

            loss = LOSS_FUNCTION(output_batched, ground_truth_batched, mask_batched)
            loss.backward()
            OPTIMIZER.step()

            # ===== COMPUTE STATISTICS, USING TORCH METRICS =====  
            # for each key, compute, add item to results dictionary
            running_results["loss"] += loss.detach().item()
            for key, func in metrics.items():
                running_results[key] += func(output_batched, ground_truth_batched, mask_batched).detach().item()

            # log with wandb
            spliced = ((-mask_batched + 1) * output_batched + input_batched[:,:-1,:,:]).detach()
            if log_wandb and (num_batches % LOG_EVERY == 0):
                batched_predictions = torch.cat((
                    input_batched[:SAMPLE_SIZE, 0:3,:,:], # can be 4 channels
                    ground_truth_batched[:SAMPLE_SIZE,:,:,:],  # 3 channels
                    nn.functional.relu(output_batched[:SAMPLE_SIZE, :,:,:]), # 3 channels
                    nn.functional.relu(spliced[:SAMPLE_SIZE,:,:,:])), dim = 0) 
                
                image_array = torchvision.utils.make_grid(batched_predictions, nrow = SAMPLE_SIZE, padding = 50)
                images = wandb.Image(
                    image_array, 
                    caption = "1st row: Damaged, 2nd row: Ground truth, 3rd row: Reconstructed")
                wandb.log( {
                    "images" : images,
                    "loss" : loss.detach().item(),
                    "lr" : OPTIMIZER.param_groups[0]['lr']
                })
        

            # ===== HOUSEKEEPING =====
            del loss
            del input_batched
            del output_batched

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



def evaluate_epoch(model, device, validation_dataloader, training_params : dict, metrics : dict):
    """
    This method encapsulates the evaluation of a given model for one epoch.
    
    @param model : nn.Module                            Model to be trained.
    @param device : str                                 Device to be trained on.
    @param validation_dataloader : nn.data.DataLoader   DataLoader object to load batches of data.
    @param training_params : dict                       Dictionary object mapping names of 
                                                        training utilities to their respective objects.
                                                        Required are "batch_size", "loss_function", 
                                                        and "optimizer". 
    @param metrics : dict                               Dictionary object mapping names of 
                                                        metrics to a functional method that 
                                                        would compute the metric value.
    """
    
    # ===== INITIALIZE =====
    # constants
    LOSS_FUNCTION = training_params["loss_function"]

    # to device
    model = model.to(device)

    # epoch statistics
    running_results = {list(metrics.keys())[i] : 0.0 for i in range(len(metrics)) } 
    running_results["loss"] = 0.0

    # ===== EVALUATE EPOCH =====

    with torch.no_grad():
        model.eval()
        batches = 0
        for index, batch in enumerate(validation_dataloader, 1):
            
            batches += 1

            # input and ground truth
            input_batched = batch["image"]
            ground_truth_batched = batch["reconstructed"]
            mask_batched = batch["mask"]

            # move tensors to device
            input_batched = input_batched.to(device)
            ground_truth_batched = ground_truth_batched.to(device)
            mask_batched = mask_batched.to(device)

            # reshape to channel first
            input_batched = input_batched.permute(0, 3, 1, 2)
            ground_truth_batched = ground_truth_batched.permute(0, 3, 1, 2)
            mask_batched = mask_batched.permute(0, 3, 1, 2)

            # predict    
            output_batched = model(input_batched)

            # evaluate
            loss = LOSS_FUNCTION(output_batched, ground_truth_batched, mask_batched).detach().item()
            running_results["loss"] += loss
            
            # ===== COMPUTE STATISTICS, USING TORCH METRICS =====
            for key, func in metrics.items():
                running_results[key] += func(output_batched, ground_truth_batched, mask_batched).detach().item()

            args = ""
            for key, val in running_results.items():
                args += key + ": " + str(running_results[key]/batches) + "   "
            print(f"\r{batches}/{len(validation_dataloader)}: " + args, end = '', flush = True)

            # delete to ensure memory footprint
            del loss
            del input_batched
            del output_batched

    # normalise numbers by batch
    for key, val in running_results.items():
        running_results[key] /= batches

    return running_results

def train_evaluate(model, device, train_dataset, validation_dataset, training_params: dict, metrics: dict, start_epoch = 0, sample_size = 16, log_every = 1):

    """
    This method encapsulates the training and evaluation loop of a given model.
    
    @param model : nn.Module                            Model to be trained.
    @param device : str                                 Device to be trained on.
    @param train_dataloader : nn.data.DataLoader        DataLoader object to load batches of data for training.
    @param validation_dataloader : nn.data.DataLoader   DataLoader object to load batches of data for validation.
    @param training_params : dict                       Dictionary object mapping names of 
                                                        training utilities to their respective objects.
                                                        Required are "num_epochs", "batch_size", "loss_function", 
                                                        "scheduler", "save_path" and "optimizer". 
    @param metrics : dict                               Dictionary object mapping names of 
                                                        metrics to a functional method that 
                                                        would compute the metric value.
    @parm start_epoch : int
    @param sample_size : int 
    @param log_every : int
    """


    # ===== INITIALIZE =====
    # constants
    NUM_EPOCHS = training_params["num_epochs"]
    BATCH_SIZE = training_params["batch_size"]
    SCHEDULER = training_params["scheduler"]
    SAVE_PATH = training_params["save_path"]
    NUM_WORKERS = 2
    START_EPOCH = start_epoch
    SAMPLE_SIZE = sample_size
    LOG_EVERY = log_every
    PLOT_EVERY = 1


    # variables
    train_results = {list(metrics.keys())[i] : [] for i in range(len(metrics)) } 
    train_results["loss"] = []
    eval_results = {list(metrics.keys())[i] : [] for i in range(len(metrics)) } 
    eval_results["loss"] = []

    # dataloaders
    train_dataloader = DataLoader(train_dataset, batch_size = BATCH_SIZE, shuffle = True, num_workers = NUM_WORKERS)
    validation_dataloader = DataLoader(validation_dataset, batch_size = BATCH_SIZE, shuffle = True, num_workers = NUM_WORKERS)

    # ===== TRAIN =====
    for epoch in range(NUM_EPOCHS):

        start = time.time()

        # train
        print(f"\n===== Epoch: {START_EPOCH + epoch + 1} ===== ")
        num_batches = 0

        # train every epoch
        print("\nTraining ...")
        results = train_epoch(model, device, train_dataloader, training_params, metrics, LOG_EVERY, SAMPLE_SIZE)
        for key, val in results.items():
            train_results[key].append(val)

        # evaluate every epoch
        print("\nEvaluating ...")
        results = evaluate_epoch(model, device, validation_dataloader, training_params, metrics)
        for key, val in results.items():
            eval_results[key].append(val)

        # ===== EPOCH RESULTS =====
        # summary
        print(f"\nCompleted epoch {START_EPOCH + epoch + 1}! Took {(time.time() - start)/60} min")

        # ===== VISUALIZE =====
        if epoch % PLOT_EVERY == 0:
            print("plotting ...")
            loader = DataLoader(validation_dataset, batch_size = SAMPLE_SIZE, shuffle = True)
            batch = next(iter(loader))

            # predict and plot
            model.eval()
            output = model(batch["image"].to(device).permute(0, 3, 1, 2)).detach().cpu().permute(0, 2, 3, 1)
            fig, ax = plt.subplots(3, SAMPLE_SIZE, figsize = (SAMPLE_SIZE * 5, 15, ))
            for i in range(SAMPLE_SIZE):
                image = batch["image"][i]
                reconstructed = batch["reconstructed"][i]
                predicted = output[i]

                if image.shape[-1] > 3: 
                    image = image[:, :, 0:3] # take rgb if more than 3 channels
                    
                ax[0][i].imshow(image)
                ax[1][i].imshow(reconstructed)
                ax[2][i].imshow(predicted)
                
            plt.savefig(f"{SAVE_PATH}_epoch{epoch + 1}.png")
            print("saved plots!")
            plt.close()

        # ===== HOUSEKEEPING =====

        # scheduler every epoch
        if SCHEDULER is not None:
            SCHEDULER.step(eval_results["loss"][epoch])

        # save save every epoch
        SAVE = f"{SAVE_PATH}_epoch{epoch + 1}.pt"
        torch.save(model.state_dict(), SAVE)
        print("saved model!")

    return train_results, eval_results