import numpy as np
from .boys import *

# ## MD4

# Se definen las relaciones de recurrencia para E (aquí se expresan las de $X$, pero hay otras equivalentes para $Y$ y $Z$).
# \begin{eqnarray}
# E_t^{i_x+1,j_x} &=& \frac{1}{2p} E^{i_x j_x}_{t-1} + X_{PA} E_t^{i_x j_x}+(t+1)E^{i_x j_x}_{t+1}\\
# E_t^{i_x,j_x+1} &=& \frac{1}{2p} E^{i_xj_x}_{t-1} + X_{PB} E_t^{i_xj_x}+(t+1)E^{i_xj_x}_{t+1}
# \end{eqnarray}
# que llegan hasta
# \begin{equation}
# E_{0}^{00} = K_{ab}^x
# \end{equation}
# 
# Estas provienen de la expansión del producto de Gaussianas cartesianas en gaussianas Hermitianas.
# \begin{equation}
# \Omega_{i_x,j_x} = g_{i_x} g_{j_x} = \sum_t^{i_x+j_x} E_{t}^{i_x,j_x} \Lambda_{t}
# \end{equation}

def compute_E(t,la,lb,pair,i,xyz):
    
    if(t<0):
        return 0
    elif(t>la+lb):
        return 0
    elif(la>0):
        E_im1j_tm1 = compute_E(t-1,la-1,lb,pair,i,xyz)
        E_im1j_t = compute_E(t,la-1,lb,pair,i,xyz)
        E_im1j_tp1 = compute_E(t+1,la-1,lb,pair,i,xyz)
        return 1/(2*pair.exp[i])*E_im1j_tm1 + (pair.coord[i][xyz]-pair.g_a.coord[xyz])*E_im1j_t + (t+1)*E_im1j_tp1
    elif(lb>0):
        E_ijm1_tm1 = compute_E(t-1,la,lb-1,pair,i,xyz)
        E_ijm1_t = compute_E(t,la,lb-1,pair,i,xyz)
        E_ijm1_tp1 = compute_E(t+1,la,lb-1,pair,i,xyz)    
        return 1/(2*pair.exp[i])*E_ijm1_tm1 + (pair.coord[i][xyz]-pair.g_b.coord[xyz])*E_ijm1_t + (t+1)*E_ijm1_tp1
    elif(t==0 and la==0 and lb==0):
        return np.exp(-pair.alpha[i]*(pair.g_b.coord[xyz]-pair.g_a.coord[xyz])**2)


# Se definen las relaciones de recurrencia
# \begin{eqnarray}
# R_{000}^n &=& -(2\alpha)^n \frac{2 \pi^{5/2}}{pq \sqrt{p+q}} F_{n}(\alpha R_{PQ}^2) \\
# R^n_{t_x+1,t_y,t_z} &=& t_x R^{n+1}_{t_x-1,t_y,t_z} + X_{PQ} R^{n+1}_{t_x,t_y,t_z} \\
# R^n_{t_x,t_y+1,t_z} &=& t_y R^{n+1}_{t_x,t_y-1,t_z} + Y_{PQ} R^{n+1}_{t_x,t_y,t_z} \\
# R^n_{t_x,t_y,t_z+1} &=& t_z R^{n+1}_{t_x,t_y,t_z-1} + Z_{PQ} R^{n+1}_{t_x,t_y,t_z} \\
# \end{eqnarray}

def R(v_x,v_y,v_z,n,pairAB,pairCD,i,j,alpha,Rpq):

    if(v_x<0 or v_y<0 or v_z<0):
        return 0
    elif(v_x!=0):
        R_np1_vm2 = R(v_x-2,v_y,v_z,n+1,pairAB,pairCD,i,j,alpha,Rpq)
        R_np1_vm1 = R(v_x-1,v_y,v_z,n+1,pairAB,pairCD,i,j,alpha,Rpq)
        return (v_x-1)*R_np1_vm2 + Rpq[0]*R_np1_vm1
    elif(v_y!=0):
        R_np1_vm2 = R(v_x,v_y-2,v_z,n+1,pairAB,pairCD,i,j,alpha,Rpq)
        R_np1_vm1 = R(v_x,v_y-1,v_z,n+1,pairAB,pairCD,i,j,alpha,Rpq)
        return (v_y-1)*R_np1_vm2 + Rpq[1]*R_np1_vm1
    elif(v_z!=0):
        R_np1_vm2 = R(v_x,v_y,v_z-2,n+1,pairAB,pairCD,i,j,alpha,Rpq)
        R_np1_vm1 = R(v_x,v_y,v_z-1,n+1,pairAB,pairCD,i,j,alpha,Rpq)
        return (v_z-1)*R_np1_vm2 + Rpq[2]*R_np1_vm1
    else:
        return (-2*alpha)**n*2*np.pi**(5/2)/(pairAB.exp[i]*pairCD.exp[j]*np.sqrt(pairAB.exp[i]+pairCD.exp[j]))*F_n(n,alpha*np.linalg.norm(Rpq)**2)


# La integral de repulsión electrónica está dada por
# \begin{equation}
# \left(g_{\mathbf{i}} (r,a,A) g_{\mathbf{j}} (r,b,B) | \frac{1}{r_{12}} | g_{\mathbf{k}} (r,c,C)g_{\mathbf{k}} (r,d,D)\right) = \sum_{t_x,t_y,t_z}^{i_x+j_x,i_y+j_y,i_z+j_z} E^{ab}_{t_xt_yt_z} \sum_{u_x,u_y,u_z}^{k_x+l_x,k_y+l_y,k_z+l_z} E_{u_xu_yu_z}^{cd} (-1)^{u_x+u_y+u_z} R_{\mathbf{t}+\mathbf{u}}(\alpha,R_{PQ})
# \end{equation}
# 
# E son las expansiones de Hermite de las distribuciones de traslape
# \begin{equation}
# E_{t}^{ij} = E_{t_x}^{i_x j_x}E_{t_y}^{i_y j_y}E_{t_z}^{i_z j_z}
# \end{equation}
# 
# y R son las integrales de Coulomb de Hermite
# \begin{equation}
# R_{\mathbf{t}}(\alpha,R_{PQ}) = \frac{2 \pi^{5/2}}{pq \sqrt{p+q}} \left(\frac{\partial}{\partial P_x}\right)^{t_x} \left(\frac{\partial}{\partial P_y}\right)^{t_y} \left(\frac{\partial}{\partial P_z}\right)^{t_z} F_0(\alpha R_{PQ}^2)
# \end{equation}
# 

def MD4(pairAB,pairCD):

    g_a = pairAB.g_a
    g_b = pairAB.g_b
    g_c = pairCD.g_a
    g_d = pairCD.g_b
    
    result = np.zeros((len(g_a.orientaciones),len(g_b.orientaciones),len(g_c.orientaciones),len(g_d.orientaciones)))
    for a,lax,lay,laz in g_a.orientaciones:
        for b,lbx,lby,lbz in g_b.orientaciones:
            for c,lcx,lcy,lcz in g_c.orientaciones:
                for d,ldx,ldy,ldz in g_d.orientaciones:
                    integral = 0.0
                    for i in range(pairAB.k):
    
                        aux7 = 0
                        for t_z in range(laz+lbz+1): 
                            Ez_ij_t = compute_E(t_z,laz,lbz,pairAB,i,2)
                            aux6 = 0    
                            for t_y in range(lay+lby+1):
                                Ey_ij_t = compute_E(t_y,lay,lby,pairAB,i,1)
                                aux5 = 0        
                                for t_x in range(lax+lbx+1):
                                    Ex_ij_t = compute_E(t_x,lax,lbx,pairAB,i,0)
                                    aux4 = 0
                                    for j in range(pairCD.k):    
                                        alpha = pairAB.exp[i]*pairCD.exp[j]/(pairAB.exp[i]+pairCD.exp[j])
                                        Rpq = pairAB.coord[i]-pairCD.coord[j]
                                        aux3 = 0
                                        for u_z in range(lcz+ldz+1):
                                            Ez_kl_u = compute_E(u_z,lcz,ldz,pairCD,j,2)
                                            aux2 = 0
                                            for u_y in range(lcy+ldy+1):
                                                Ey_kl_u = compute_E(u_y,lcy,ldy,pairCD,j,1)
                                                aux1 = 0
                                                for u_x in range(lcx+ldx+1):
                                                    Ex_kl_u = compute_E(u_x,lcx,ldx,pairCD,j,0)
                                                    aux1 += (-1)**(u_x+u_y+u_z)*Ex_kl_u*R(t_x+u_x,t_y+u_y,t_z+u_z,0,pairAB,pairCD,i,j,alpha,Rpq)
                                                aux2 += Ey_kl_u*aux1
                                            aux3 += Ez_kl_u*aux2
                                        aux4 += aux3*pairCD.coef[j]
                                    aux5 += Ex_ij_t*aux4
                                aux6 += Ey_ij_t*aux5
                            aux7 += Ez_ij_t*aux6
                        integral += aux7*pairAB.coef[i]
                                
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result

# ## MD2

# En este esquema se usa una relación de reucrrencia horizontal para pasar la información del segundo centro al primero, y del cuarto centro al tercero. Posteriormente se obtienen las integrales $(i 0 | k 0)$ a partri de hermitianas con la relación de recurrencia vertical de MD.
# 
# Se usan los coeficientes de expansión
# \begin{equation}
# E_{t}^{i0} = E_{t_x}^{i_x 0}E_{t_y}^{i_y 0}E_{t_z}^{i_z 0}
# \end{equation}

def VRR_MD2(ii,jj,kk,ll,pairAB,pairCD):

    integral = 0.0
    for i in range(pairAB.k):
        aux7 = 0
        for t_z in range(ii[2]+1): 
            Ez_ij_t = compute_E(t_z,ii[2],0,pairAB,i,2)
            aux6 = 0    
            for t_y in range(ii[1]+1):
                Ey_ij_t = compute_E(t_y,ii[1],0,pairAB,i,1)
                aux5 = 0        
                for t_x in range(ii[0]+1):
                    Ex_ij_t = compute_E(t_x,ii[0],0,pairAB,i,0)
                    aux4 = 0
                    for j in range(pairCD.k):    
                        alpha = pairAB.exp[i]*pairCD.exp[j]/(pairAB.exp[i]+pairCD.exp[j])
                        Rpq = pairAB.coord[i]-pairCD.coord[j]
                        aux3 = 0
                        for u_z in range(kk[2]+1):
                            Ez_kl_u = compute_E(u_z,kk[2],0,pairCD,j,2)
                            aux2 = 0
                            for u_y in range(kk[1]+1):
                                Ey_kl_u = compute_E(u_y,kk[1],0,pairCD,j,1)
                                aux1 = 0
                                for u_x in range(kk[0]+1):
                                    Ex_kl_u = compute_E(u_x,kk[0],0,pairCD,j,0)
                                    aux1 += (-1)**(u_x+u_y+u_z)*Ex_kl_u*R(t_x+u_x,t_y+u_y,t_z+u_z,0,pairAB,pairCD,i,j,alpha,Rpq)
                                aux2 += Ey_kl_u*aux1
                            aux3 += Ez_kl_u*aux2
                        aux4 += aux3*pairCD.coef[j]
                    aux5 += Ex_ij_t*aux4
                aux6 += Ey_ij_t*aux5
            aux7 += Ez_ij_t*aux6
        integral += aux7*pairAB.coef[i]
            
    return integral


# y se define la relación de recurrencia horizontal (aquí se expresan las de $X$, pero hay otras equivalentes para $Y$ y $Z$).
# \begin{eqnarray}
# \Theta^N_{i,j+1,k,l} &=& \Theta^N_{i+1,j,k,l} + X_{AB}\Theta_{i,j,k,l}^N\\
# \Theta^N_{i,j,k,l+1} &=& \Theta^N_{i,j,k+1,l} + X_{CD}\Theta_{i,j,k,l}^N
# \end{eqnarray}

def HRR_MD2(i,j,k,l,pairAB,pairCD):

    for xyz in range(3):
        if(l[xyz]!=0):
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            kp1 = k[:]
            kp1[xyz] = kp1[xyz] + 1
            return HRR_MD2(i,j,kp1,lm1,pairAB,pairCD) + (pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])*HRR_MD2(i,j,k,lm1,pairAB,pairCD)
        elif(j[xyz]!=0):
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            ip1 = i[:]
            ip1[xyz] = ip1[xyz] + 1
            return HRR_MD2(ip1,jm1,k,l,pairAB,pairCD) + (pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])*HRR_MD2(i,jm1,k,l,pairAB,pairCD)
    return VRR_MD2(i,j,k,l,pairAB,pairCD)

def MD2(pairAB,pairCD):

    g_a = pairAB.g_a
    g_b = pairAB.g_b
    g_c = pairCD.g_a
    g_d = pairCD.g_b

    result = np.zeros((len(g_a.orientaciones),len(g_b.orientaciones),len(g_c.orientaciones),len(g_d.orientaciones)))
    for a,lax,lay,laz in g_a.orientaciones:
        for b,lbx,lby,lbz in g_b.orientaciones:
            for c,lcx,lcy,lcz in g_c.orientaciones:
                for d,ldx,ldy,ldz in g_d.orientaciones:
                    
                    i = [lax,lay,laz]
                    j = [lbx,lby,lbz]
                    k = [lcx,lcy,lcz]
                    l = [ldx,ldy,ldz]
                    integral = HRR_MD2(i,j,k,l,pairAB,pairCD)
                    
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result


# # MD1

# Se usa la relación de recurrencia de transferencia de electrones para pasar la información del tercer centro al primer centro.
# 
# \begin{eqnarray}
# \Theta_{i,0,k+1,0}^N &=& - \frac{b X_{AB} + dX_{CD}}{q} \Theta_{i,0,k,0}^{N} + \frac{i}{2q}\Theta^{N}_{i-1,0,k,0} + \frac{k}{2q} \Theta^N_{i,0,k-1,0} - \frac{p}{q} \Theta^N_{i+1,0,k,0}
# \end{eqnarray}

def VRR_MD1(ii,jj,kk,ll,pairAB,pairCD,i,j):


    alpha = pairAB.exp[i]*pairCD.exp[j]/(pairAB.exp[i]+pairCD.exp[j])
    Rpq = pairAB.coord[i]-pairCD.coord[j]

    integral = 0.0
    for t_z in range(ii[2]+1):
        Ez_ij_t = compute_E(t_z,ii[2],0,pairAB,i,2)
        aux5 = 0
        for t_y in range(ii[1]+1):
            Ey_ij_t = compute_E(t_y,ii[1],0,pairAB,i,1)
            aux4 = 0
            for t_x in range(ii[0]+1):
                Ex_ij_t = compute_E(t_x,ii[0],0,pairAB,i,0)
                aux3 = 0
                for u_z in range(kk[2]+1):
                    Ez_kl_u = compute_E(u_z,kk[2],0,pairCD,j,2)
                    aux2 = 0
                    for u_y in range(kk[1]+1):
                        Ey_kl_u = compute_E(u_y,kk[1],0,pairCD,j,1)
                        aux1 = 0
                        for u_x in range(kk[0]+1):
                            Ex_kl_u = compute_E(u_x,kk[0],0,pairCD,j,0)
                            aux1 += (-1)**(u_x+u_y+u_z)*Ex_kl_u*R(t_x+u_x,t_y+u_y,t_z+u_z,0,pairAB,pairCD,i,j,alpha,Rpq)
                        aux2 += Ey_kl_u*aux1
                    aux3 += Ez_kl_u*aux2
                aux4 += Ex_ij_t*aux3
            aux5 += Ey_ij_t*aux4
        integral += Ez_ij_t*aux5

    return integral

def trans_elec_MD1(i,j,k,l,pairAB,pairCD,ii,jj):

    integral = 0.0
    
    for xyz in range(3):
        if(i[xyz]<0 or k[xyz]<0):
            return 0
        elif(k[xyz]!=0):
            km1 = k[:]
            km1[xyz] = km1[xyz] - 1 
            km2 = k[:]
            km2[xyz] = km2[xyz] - 2 
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1         
            ip1 = i[:]
            ip1[xyz] = ip1[xyz] + 1        
            return -(pairAB.ab[ii][1]*(pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])+pairCD.ab[jj][1]*(pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz]))/pairCD.exp[jj]*trans_elec_MD1(i,j,km1,l,pairAB,pairCD,ii,jj) + i[xyz]/(2*pairCD.exp[jj])*trans_elec_MD1(im1,j,km1,l,pairAB,pairCD,ii,jj) + (k[xyz]-1)/(2*pairCD.exp[jj])*trans_elec_MD1(i,j,km2,l,pairAB,pairCD,ii,jj) - pairAB.exp[ii]/pairCD.exp[jj]*trans_elec_MD1(ip1,j,km1,l,pairAB,pairCD,ii,jj)
    return VRR_MD1(i,j,k,l,pairAB,pairCD,ii,jj)


def HRR_MD1(i,j,k,l,pairAB,pairCD):

    for xyz in range(3):
        if(l[xyz]!=0):
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            kp1 = k[:]
            kp1[xyz] = kp1[xyz] + 1
            return HRR_MD1(i,j,kp1,lm1,pairAB,pairCD) + (pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])*HRR_MD1(i,j,k,lm1,pairAB,pairCD)
        elif(j[xyz]!=0):
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            ip1 = i[:]
            ip1[xyz] = ip1[xyz] + 1
            return HRR_MD1(ip1,jm1,k,l,pairAB,pairCD) + (pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])*HRR_MD1(i,jm1,k,l,pairAB,pairCD)

    integral = 0.0
    for ii in range(pairAB.k):
        aux1 = 0.0
        for jj in range(pairCD.k):
            aux1 += trans_elec_MD1(i,j,k,l,pairAB,pairCD,ii,jj)*pairCD.coef[jj]
        integral += aux1*pairAB.coef[ii]
    return integral

def MD1(pairAB,pairCD):

    g_a = pairAB.g_a
    g_b = pairAB.g_b
    g_c = pairCD.g_a
    g_d = pairCD.g_b

    result = np.zeros((len(g_a.orientaciones),len(g_b.orientaciones),len(g_c.orientaciones),len(g_d.orientaciones)))
    for a,lax,lay,laz in g_a.orientaciones:
        for b,lbx,lby,lbz in g_b.orientaciones:
            for c,lcx,lcy,lcz in g_c.orientaciones:
                for d,ldx,ldy,ldz in g_d.orientaciones:
                    
                    i = [lax,lay,laz]
                    j = [lbx,lby,lbz]
                    k = [lcx,lcy,lcz]
                    l = [ldx,ldy,ldz]
                    integral = HRR_MD1(i,j,k,l,pairAB,pairCD)
                    
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result
