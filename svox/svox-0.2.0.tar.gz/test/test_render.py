import svox
import torch
import torch.cuda
import matplotlib.pyplot as plt

device = 'cuda:0'

t = svox.N3Tree.load("/home/sxyu/proj/volrend/build/nerf_synthetic/lego_sm.npz",
                      map_location=device)
r = svox.VolumeRenderer(t)
sqrt_2 = 2 ** -0.5
c2w = torch.tensor([[0.0, -sqrt_2, sqrt_2, -1.7],
                    [-1.0, 0.0,    0.0,     0.0],
                    [0.0, -sqrt_2, -sqrt_2, 1.7]], device=device)


start = torch.cuda.Event(enable_timing=True)
end = torch.cuda.Event(enable_timing=True)

AVG_TIMES = 5

start.record()
for i in range(AVG_TIMES):
    im = r.render_persp(c2w, height=400, width=400, fx=300)
end.record()

torch.cuda.synchronize(device)
dur = start.elapsed_time(end) / AVG_TIMES
print('render time', dur, 'ms =', 1000 / dur, 'fps')
print(im.shape)

rgb = im[..., :3].cpu()
alpha = im[..., 3].cpu()
rgb.clamp_(0.0, 1.0)
plt.figure()
plt.subplot(2, 1, 1)
plt.imshow(rgb)
plt.subplot(2, 1, 2)
plt.imshow(alpha)
plt.show()
