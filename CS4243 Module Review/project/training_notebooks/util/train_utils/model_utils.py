import torch
import torch.nn as nn


# ===== CUSTOM LAYERS =====

class Conv2dBlock(nn.Module):
    """
    This class encapsulates a standard convolution block.
    Conv -> BN -> activation
    """

    def __init__(self, input_dim, output_dim, 
        kernel_size = 3, stride = 1, padding = 'same', dilation = 1, 
        activation = nn.ReLU):

        super(Conv2dBlock, self).__init__()

        self.conv = nn.Conv2d(input_dim, output_dim, kernel_size, stride, padding, dilation)
        self.bn = nn.BatchNorm2d(output_dim)
        self.activation = activation()


    def forward(self, input_tensor):
        
        x = input_tensor
        x = self.conv(x)
        x = self.bn(x)
        x = self.activation(x)

        return x

class UpConv2dBlock(nn.Module):
    """
    This class encapsulates upsampling by upsampling then convolution. 
    Here is a reference of this technique compared to transposed convolutions:
    Odena, et al., "Deconvolution and Checkerboard Artifacts", Distill, 2016. http://doi.org/10.23915/distill.00003
    """

    def __init__(self, input_dim, output_dim, 
        kernel_size = 3, stride = 1, padding = 'same', dilation = 1, 
        activation = nn.ReLU, 
        scale_factor = (2,2), mode = 'nearest'):

        super(UpConv2dBlock, self).__init__()
        self.upsample = nn.Upsample(scale_factor = scale_factor, mode = mode)
        self.conv = nn.Conv2d(input_dim, output_dim, kernel_size, stride, padding, dilation)
        self.activation = activation()
        self.bn = nn.BatchNorm2d(output_dim)

    def forward(self, input_tensor):
        
        x = input_tensor
        x = self.upsample(x)
        x = self.conv(x)
        x = self.bn(x)
        x = self.activation(x)

        return x


class LinearBlock(nn.Module):
    """
    This class encapsulates a linear layer. 
    Linear -> BN -> activation
    """

    def __init__(self, input_dim, output_dim, activation = nn.ReLU):
        super(LinearBlock, self).__init__()

        self.linear = nn.Linear(input_dim, output_dim)
        self.activation = activation()
        self.bn = nn.BatchNorm1d(output_dim)

    def forward(self, input_tensor):
        
        x = input_tensor
        x = self.linear(x)
        x = self.bn(x)
        x = self.activation(x)

        return x

class GatedConv2d(nn.Module):

    """
    This class implements a gated convolution, following the implementation in the given reference.
    """

    def __init__(self, in_channels, out_channels, kernel_size, stride, padding, dilation):
        super(GatedConv2d, self).__init__()
        self.image_conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation = dilation)
        self.gate_conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, dilation = dilation)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_tensor, return_mask = False):

        mask = self.sigmoid(self.gate_conv(input_tensor))
        x = self.image_conv(input_tensor)
        x = torch.mul(x, mask) # apply mask

        if return_mask:
            return x, mask

        return x

class GatedUpConv2dBlock(nn.Module):

    def __init__(self, input_dim, output_dim, 
        kernel_size = 3, stride = 1, padding = 'same', dilation = 1, 
        activation = nn.ReLU, 
        scale_factor = (2,2), mode = 'nearest'):

        super(GatedUpConv2dBlock, self).__init__()


        self.upsample = nn.Upsample(scale_factor = scale_factor, mode = mode)
        self.conv = GatedConv2d(input_dim, output_dim, kernel_size, stride, padding, dilation)
        self.activation = activation()
        self.bn = nn.BatchNorm2d(output_dim)

    def forward(self, input_tensor):
        
        x = input_tensor
        x = self.upsample(x)
        x = self.conv(x)
        x = self.bn(x)
        x = self.activation(x)

        return x

class GatedConv2dBlock(nn.Module):
    """
    This class encapsulates a standard convolution block.
    Conv -> BN -> activation
    """

    def __init__(self, input_dim, output_dim, 
        kernel_size = 3, stride = 1, padding = 'same', dilation = 1, 
        activation = nn.ReLU):

        super(GatedConv2dBlock, self).__init__()

        self.conv = GatedConv2d(input_dim, output_dim, kernel_size, stride, padding, dilation)
        self.bn = nn.BatchNorm2d(output_dim)
        self.activation = activation()


    def forward(self, input_tensor):
        
        x = input_tensor
        x = self.conv(x)
        x = self.bn(x)
        x = self.activation(x)

        return x