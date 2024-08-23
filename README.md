# 3D/2D Registration of Angiograms using Silhouette-based Differentiable Rendering
Registration of a 3D mesh derived from MRA, CTA or 3d DSA onto two images of 2D DSA using silhouette-based differentiable rendering.



![Registration](./img/visu_skel.png)

## Build

The pose estimation is based on PyTorch3D differentiable rendering.
The visualizer is based on PyVitsa.

- PyTorch3D version ...
- PyVitsa version ...

## Usage
- Inputs: 3D Mesh + Two DSA images, antero-posterior and lateral
- Outputs: Camera pose Rotation and translation

## Ressources
We used this dataset of paired 3D/2D DSA images: https://lit.fe.uni-lj.si/en/research/resources/3D-2D-GS-CA/


## Publication

If you find this code useful for your research, please cite the following paper:
