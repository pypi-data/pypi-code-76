import torch
import torch.nn.functional as F
import sve

device='cuda:0'
K = 4

g = sve.N3Tree(N=2).to(device=device)

for i in range(10):
    q = torch.rand((1, 3), device=device)
    vals = torch.randn((1, K), device=device)
    g.set(q, vals, cuda=True)

g.refine_at(0, (0, 0, 0))
q = torch.tensor([[0.9,0.9,0.9], [0.49, 0.49, 0.49]], device=device)
vals = torch.tensor([[0.0, 1.0, 1.0, 10.0], [1.0, 0.49, 0.49, 0.49]], device=device)
g.set(q, vals, cuda=True)
r=g.get(q, cuda=True)
print(r.detach().cpu().numpy())
print(vals.cpu().numpy())

