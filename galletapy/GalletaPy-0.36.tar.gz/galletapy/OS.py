import numpy as np
from .boys import *

# ## OS4
# Se usa la relación de recurrencia
# \begin{eqnarray}
# \Theta_{i+1,j,k,l}^N &=& X_{PA}\Theta_{ijkl}^N - \frac{\alpha}{p}X_{PQ} \Theta_{ijkl}^{N+1} + \frac{i}{2p} \left( \Theta_{i-1,j,k,l}^N - \frac{\alpha}{p} \Theta_{i-1,j,k,l}^{N+1}\right) + \frac{j}{2p} \left( \Theta_{i,j-1,k,l}^N - \frac{\alpha}{p} \Theta_{i,j-1,k,l}^{N+1}\right) + \frac{k}{2(p+q)} \left( \Theta_{i,j,k-1,l}^{N+1}\right) + \frac{l}{2(p+q)} \left( \Theta_{i,j,k,l-1}^{N+1}\right) \\
# \Theta_{i,j+1,k,l}^N &=& X_{PB}\Theta_{ijkl}^N - \frac{\alpha}{p}X_{PQ} \Theta_{ijkl}^{N+1} + \frac{j}{2p} \left( \Theta_{i,j-1,k,l}^N - \frac{\alpha}{p} \Theta_{i,j-1,k,l}^{N+1}\right) + \frac{i}{2p} \left( \Theta_{i-1,j,k,l}^N - \frac{\alpha}{p} \Theta_{i-1,j,k,l}^{N+1}\right) + \frac{k}{2(p+q)} \left( \Theta_{i,j,k-1,l}^{N+1}\right) + \frac{l}{2(p+q)} \left( \Theta_{i,j,k,l-1}^{N+1}\right) \\
# \Theta_{i,j,k+1,l}^N &=& X_{QC}\Theta_{ijkl}^N - \frac{\alpha}{q}X_{PQ} \Theta_{ijkl}^{N+1} + \frac{k}{2q} \left( \Theta_{i,j,k-1,l}^N - \frac{\alpha}{q} \Theta_{i,j,k-1,l}^{N+1}\right) + \frac{l}{2q} \left( \Theta_{i,j,k,l-1}^N - \frac{\alpha}{q} \Theta_{i,j,k,l-1}^{N+1}\right) + \frac{i}{2(p+q)} \left( \Theta_{i-1,j,k,l}^{N+1}\right) + \frac{j}{2(p+q)} \left( \Theta_{i,j-1,k,l}^{N+1}\right) \\
# \Theta_{i,j,k,l+1}^N &=& X_{QD}\Theta_{ijkl}^N - \frac{\alpha}{q}X_{PQ} \Theta_{ijkl}^{N+1} + \frac{l}{2q} \left( \Theta_{i,j,k,l-1}^N - \frac{\alpha}{q} \Theta_{i,j,k,l-1}^{N+1}\right) + \frac{k}{2q} \left( \Theta_{i,j,k-1,l}^N - \frac{\alpha}{q} \Theta_{i,j,k-1,l}^{N+1}\right) + \frac{i}{2(p+q)} \left( \Theta_{i-1,j,k,l}^{N+1}\right) + \frac{j}{2(p+q)} \left( \Theta_{i,j-1,k,l}^{N+1}\right) \\
# \end{eqnarray}

def VRR_OS4(pairAB,pairCD,i,j,k,l,N,ii,jj):

    alpha = pairAB.exp[ii]*pairCD.exp[jj]/(pairAB.exp[ii]+pairCD.exp[jj])

    for xyz in range(3):
        if(i[xyz]<0 or j[xyz]<0 or k[xyz]<0 or l[xyz]<0):
            return 0
        elif(i[xyz]>0):
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1
            im2 = i[:]
            im2[xyz] = im2[xyz] - 2
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            km1 = k[:]
            km1[xyz] = km1[xyz] - 1
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            return (pairAB.coord[ii][xyz]-pairAB.g_a.coord[xyz])*VRR_OS4(pairAB,pairCD,im1,j,k,l,N,ii,jj) - alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*VRR_OS4(pairAB,pairCD,im1,j,k,l,N+1,ii,jj) + (i[xyz]-1)/(2*pairAB.exp[ii])*(VRR_OS4(pairAB,pairCD,im2,j,k,l,N,ii,jj) - alpha/pairAB.exp[ii]*VRR_OS4(pairAB,pairCD,im2,j,k,l,N+1,ii,jj)) + (j[xyz])/(2*pairAB.exp[ii])*(VRR_OS4(pairAB,pairCD,im1,jm1,k,l,N,ii,jj) - alpha/pairAB.exp[ii]*VRR_OS4(pairAB,pairCD,im1,jm1,k,l,N+1,ii,jj)) + (k[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,im1,j,km1,l,N+1,ii,jj)) + (l[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,im1,j,k,lm1,N+1,ii,jj))
        elif(j[xyz]>0):
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            jm2 = j[:]
            jm2[xyz] = jm2[xyz] - 2
            km1 = k[:]
            km1[xyz] = km1[xyz] - 1
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            return (pairAB.coord[ii][xyz]-pairAB.g_b.coord[xyz])*VRR_OS4(pairAB,pairCD,i,jm1,k,l,N,ii,jj) - alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*VRR_OS4(pairAB,pairCD,i,jm1,k,l,N+1,ii,jj) + (j[xyz]-1)/(2*pairAB.exp[ii])*(VRR_OS4(pairAB,pairCD,i,jm2,k,l,N,ii,jj) - alpha/pairAB.exp[ii]*VRR_OS4(pairAB,pairCD,i,jm2,k,l,N+1,ii,jj)) + (i[xyz])/(2*pairAB.exp[ii])*(VRR_OS4(pairAB,pairCD,im1,jm1,k,l,N,ii,jj) - alpha/pairAB.exp[ii]*VRR_OS4(pairAB,pairCD,im1,jm1,k,l,N+1,ii,jj)) + (k[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,i,jm1,km1,l,N+1,ii,jj)) + (l[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,i,jm1,k,lm1,N+1,ii,jj))
        elif(k[xyz]>0):
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            km1 = k[:]
            km1[xyz] = km1[xyz] - 1
            km2 = k[:]
            km2[xyz] = km2[xyz] - 2
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            return (pairCD.coord[jj][xyz]-pairCD.g_a.coord[xyz])*VRR_OS4(pairAB,pairCD,i,j,km1,l,N,ii,jj) + alpha/pairCD.exp[jj]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*VRR_OS4(pairAB,pairCD,i,j,km1,l,N+1,ii,jj) + (k[xyz]-1)/(2*pairCD.exp[jj])*(VRR_OS4(pairAB,pairCD,i,j,km2,l,N,ii,jj) - alpha/pairCD.exp[jj]*VRR_OS4(pairAB,pairCD,i,j,km2,l,N+1,ii,jj)) + (l[xyz])/(2*pairCD.exp[jj])*(VRR_OS4(pairAB,pairCD,i,j,km1,lm1,N,ii,jj) - alpha/pairCD.exp[jj]*VRR_OS4(pairAB,pairCD,i,j,km1,lm1,N+1,ii,jj)) + (i[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,im1,j,km1,l,N+1,ii,jj)) + (j[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,i,jm1,km1,l,N+1,ii,jj))
        elif(l[xyz]>0):
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            km1 = k[:]
            km1[xyz] = km1[xyz] - 1
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            lm2 = l[:]
            lm2[xyz] = lm2[xyz] - 2
            return (pairCD.coord[jj][xyz]-pairCD.g_b.coord[xyz])*VRR_OS4(pairAB,pairCD,i,j,k,lm1,N,ii,jj) + alpha/pairCD.exp[jj]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*VRR_OS4(pairAB,pairCD,i,j,k,lm1,N+1,ii,jj) + (l[xyz]-1)/(2*pairCD.exp[jj])*(VRR_OS4(pairAB,pairCD,i,j,k,lm2,N,ii,jj) - alpha/pairCD.exp[jj]*VRR_OS4(pairAB,pairCD,i,j,k,lm2,N+1,ii,jj)) + (k[xyz])/(2*pairCD.exp[jj])*(VRR_OS4(pairAB,pairCD,i,j,km1,lm1,N,ii,jj) - alpha/pairCD.exp[jj]*VRR_OS4(pairAB,pairCD,i,j,km1,lm1,N+1,ii,jj)) + (i[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,im1,j,k,lm1,N+1,ii,jj)) + (j[xyz])/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(VRR_OS4(pairAB,pairCD,i,jm1,k,lm1,N+1,ii,jj))
        
    RAB = np.linalg.norm(pairAB.g_a.coord-pairAB.g_b.coord)
    RCD = np.linalg.norm(pairCD.g_a.coord-pairCD.g_b.coord)
    RPQ = np.linalg.norm(pairAB.coord[ii]-pairCD.coord[jj])
    return 2*np.pi**(5/2)/(pairAB.exp[ii]*pairCD.exp[jj]*np.sqrt(pairAB.exp[ii]+pairCD.exp[jj]))*np.exp(-pairAB.alpha[ii]*RAB**2)*np.exp(-pairCD.alpha[jj]*RCD**2)*F_n(N,alpha*RPQ**2)        

def OS4(pairAB,pairCD):

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
                    for ii in range(pairAB.k):
                        aux1 = 0.0
                        for jj in range(pairCD.k):
                                
                            i = [lax,lay,laz]
                            j = [lbx,lby,lbz]
                            k = [lcx,lcy,lcz]
                            l = [ldx,ldy,ldz]
                            aux1 += VRR_OS4(pairAB,pairCD,i,j,k,l,0,ii,jj)*pairCD.coef[jj]
                        integral += aux1*pairAB.coef[ii]
                    
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result


# ## OS2

# Aquí se aprovecha la relación de recurrencia horizontal.
# 
# Primero se planea construir la parte vertical hacia el primer y tercer centro

def VRR_OS2(i,j,k,l,N,pairAB,pairCD,ii,jj):

    alpha = pairAB.exp[ii]*pairCD.exp[jj]/(pairAB.exp[ii]+pairCD.exp[jj])

    for xyz in range(3):
        if(i[xyz]<0 or k[xyz]<0):
            return 0
        elif(i[xyz]>0):
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1
            im2 = i[:]
            im2[xyz] = im2[xyz] - 2
            km1 = k[:]
            km1[xyz] = km1[xyz] - 1
            return (pairAB.coord[ii][xyz]-pairAB.g_a.coord[xyz])*VRR_OS2(im1,j,k,l,N,pairAB,pairCD,ii,jj) - alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*VRR_OS2(im1,j,k,l,N+1,pairAB,pairCD,ii,jj) + (i[xyz]-1)/(2*pairAB.exp[ii])*(VRR_OS2(im2,j,k,l,N,pairAB,pairCD,ii,jj) - alpha/pairAB.exp[ii]*VRR_OS2(im2,j,k,l,N+1,pairAB,pairCD,ii,jj)) + k[xyz]/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*VRR_OS2(im1,j,km1,l,N+1,pairAB,pairCD,ii,jj)
        elif(k[xyz]>0):
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1
            km1 = k[:]
            km1[xyz] = km1[xyz] - 1
            km2 = k[:]
            km2[xyz] = km2[xyz] - 2
            return (pairCD.coord[jj][xyz]-pairCD.g_a.coord[xyz])*VRR_OS2(i,j,km1,l,N,pairAB,pairCD,ii,jj) + alpha/pairCD.exp[jj]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*VRR_OS2(i,j,km1,l,N+1,pairAB,pairCD,ii,jj) + (k[xyz]-1)/(2*pairCD.exp[jj])*(VRR_OS2(i,j,km2,l,N,pairAB,pairCD,ii,jj) - alpha/pairCD.exp[jj]*VRR_OS2(i,j,km2,l,N+1,pairAB,pairCD,ii,jj)) + i[xyz]/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*VRR_OS2(im1,j,km1,l,N+1,pairAB,pairCD,ii,jj)

    RAB = np.linalg.norm(pairAB.g_a.coord-pairAB.g_b.coord)
    RCD = np.linalg.norm(pairCD.g_a.coord-pairCD.g_b.coord)
    RPQ = np.linalg.norm(pairAB.coord[ii]-pairCD.coord[jj])
    return 2*np.pi**(5/2)/(pairAB.exp[ii]*pairCD.exp[jj]*np.sqrt(pairAB.exp[ii]+pairCD.exp[jj]))*np.exp(-pairAB.alpha[ii]*RAB**2)*np.exp(-pairCD.alpha[jj]*RCD**2)*F_n(N,alpha*RPQ**2)

# Posteriormente se usa la horizontal para redirigir hacia el segundo y cuarto centro
# 
# \begin{eqnarray}
# \Theta^N_{i,j+1,k,l} &=& \Theta^N_{i+1,j,k,l} + X_{AB}\Theta_{i,j,k,l}^N\\
# \Theta^N_{i,j,k,l+1} &=& \Theta^N_{i,j,k+1,l} + X_{CD}\Theta_{i,j,k,l}^N
# \end{eqnarray}

def HRR_OS2(pairAB,pairCD,i,j,k,l,N):

    for xyz in range(3):
        if(l[xyz]!=0):
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            kp1 = k[:]
            kp1[xyz] = kp1[xyz] + 1
            return HRR_OS2(pairAB,pairCD,i,j,kp1,lm1,N) + (pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])*HRR_OS2(pairAB,pairCD,i,j,k,lm1,N)
        elif(j[xyz]!=0):
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            ip1 = i[:]
            ip1[xyz] = ip1[xyz] + 1
            return HRR_OS2(pairAB,pairCD,ip1,jm1,k,l,N) + (pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])*HRR_OS2(pairAB,pairCD,i,jm1,k,l,N)
    
    integral = 0.0
    for ii in range(pairAB.k):
        aux1 = 0.0
        for jj in range(pairCD.k):
                    
            aux1 += VRR_OS2(i,j,k,l,N,pairAB,pairCD,ii,jj)*pairCD.coef[jj]
        integral += aux1*pairAB.coef[ii]    
    
    return integral


def OS2(pairAB,pairCD):

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
                    integral = HRR_OS2(pairAB,pairCD,i,j,k,l,0)
                    
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result


# ## OS1

# Se define la relación de recurrencia de Obara-Saika (aquí se expresan las de $X$, pero hay otras equivalentes para $Y$ y $Z$).
# \begin{eqnarray}
# \Theta_{i+1,0,0,0}^N &=& X_{PA}\Theta_{i000}^N - \frac{\alpha}{p}X_{PQ} \Theta_{i000}^{N+1} + \frac{i}{2p} \left( \Theta_{i-1,0,0,0}^N - \frac{\alpha}{p} \Theta_{i-1,0,0,0}^{N+1}\right)
# \end{eqnarray}

def VRR_OS1(i,j,k,l,N,pairAB,pairCD,ii,jj):

    alpha = pairAB.exp[ii]*pairCD.exp[jj]/(pairAB.exp[ii]+pairCD.exp[jj])

    for xyz in range(3):
        if(i[xyz]<0):
            return 0
        elif(i[xyz]>0):
            im1 = i[:]
            im1[xyz] = im1[xyz] - 1
            im2 = i[:]
            im2[xyz] = im2[xyz] - 2
            return (pairAB.coord[ii][xyz]-pairAB.g_a.coord[xyz])*VRR_OS1(im1,j,k,l,N,pairAB,pairCD,ii,jj) - alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*VRR_OS1(im1,j,k,l,N+1,pairAB,pairCD,ii,jj) + (i[xyz]-1)/(2*pairAB.exp[ii])*(VRR_OS1(im2,j,k,l,N,pairAB,pairCD,ii,jj) - alpha/pairAB.exp[ii]*VRR_OS1(im2,j,k,l,N+1,pairAB,pairCD,ii,jj))
        
    RAB = np.linalg.norm(pairAB.g_a.coord-pairAB.g_b.coord)
    RCD = np.linalg.norm(pairCD.g_a.coord-pairCD.g_b.coord)
    RPQ = np.linalg.norm(pairAB.coord[ii]-pairCD.coord[jj])
    return 2*np.pi**(5/2)/(pairAB.exp[ii]*pairCD.exp[jj]*np.sqrt(pairAB.exp[ii]+pairCD.exp[jj]))*np.exp(-pairAB.alpha[ii]*RAB**2)*np.exp(-pairCD.alpha[jj]*RCD**2)*F_n(N,alpha*RPQ**2)                


# Se define la relación de recurrencia de Obara-Saika para transferencia de electrones (aquí se expresan las de $X$, pero hay otras equivalentes para $Y$ y $Z$).
# \begin{eqnarray}
# \Theta_{i,0,k+1,0}^N &=& - \frac{b X_{AB} + dX_{CD}}{q} \Theta_{i,0,k,0}^{N} + \frac{i}{2q}\Theta^{N}_{i-1,0,k,0} + \frac{k}{2q} \Theta^N_{i,0,k-1,0} - \frac{p}{q} \Theta^N_{i+1,0,k,0}
# \end{eqnarray}

def trans_elec_OS1(i,j,k,l,N,pairAB,pairCD,ii,jj):

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
            return -(pairAB.ab[ii][1]*(pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])+pairCD.ab[jj][1]*(pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz]))/pairCD.exp[jj]*trans_elec_OS1(i,j,km1,l,N,pairAB,pairCD,ii,jj) + i[xyz]/(2*pairCD.exp[jj])*trans_elec_OS1(im1,j,km1,l,N,pairAB,pairCD,ii,jj) + (k[xyz]-1)/(2*pairCD.exp[jj])*trans_elec_OS1(i,j,km2,l,N,pairAB,pairCD,ii,jj) - pairAB.exp[ii]/pairCD.exp[jj]*trans_elec_OS1(ip1,j,km1,l,N,pairAB,pairCD,ii,jj)
    return VRR_OS1(i,j,k,l,N,pairAB,pairCD,ii,jj)


# Se define la relación de recurrencia horizontal (aquí se expresan las de $X$, pero hay otras equivalentes para $Y$ y $Z$).
# \begin{eqnarray}
# \Theta^N_{i,j+1,k,l} &=& \Theta^N_{i+1,j,k,l} + X_{AB}\Theta_{i,j,k,l}^N\\
# \Theta^N_{i,j,k,l+1} &=& \Theta^N_{i,j,k+1,l} + X_{CD}\Theta_{i,j,k,l}^N
# \end{eqnarray}

def HRR_OS1(i,j,k,l,N,pairAB,pairCD):

    for xyz in range(3):
        if(l[xyz]!=0):
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            kp1 = k[:]
            kp1[xyz] = kp1[xyz] + 1
            return HRR_OS1(i,j,kp1,lm1,N,pairAB,pairCD) + (pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])*HRR_OS1(i,j,k,lm1,N,pairAB,pairCD)
        elif(j[xyz]!=0):
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            ip1 = i[:]
            ip1[xyz] = ip1[xyz] + 1
            return HRR_OS1(ip1,jm1,k,l,N,pairAB,pairCD) + (pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])*HRR_OS1(i,jm1,k,l,N,pairAB,pairCD)

    integral = 0.0
    for ii in range(pairAB.k):
        aux1 = 0.0
        for jj in range(pairCD.k):
            aux1 += trans_elec_OS1(i,j,k,l,N,pairAB,pairCD,ii,jj)*pairCD.coef[jj]
        integral += aux1*pairAB.coef[ii]
    return integral

# La integral de repulsión electrónica está dada por
# \begin{equation}
# \left(g_{\mathbf{i}} (r,a,A) g_{\mathbf{j}} (r,b,B) | \frac{1}{r_{12}} | g_{\mathbf{k}} (r,c,C)g_{\mathbf{k}} (r,d,D)\right)
# \end{equation}
# 
# **Tip.** Para mayor eficiencia, evaluar todas las F_n desde 0 hasta |i|+|j|+|k|+|l| al inicio y guardarlas en un vector.

def OS1(pairAB,pairCD):

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
                    integral = HRR_OS1(i,j,k,l,0,pairAB,pairCD)
                    
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result
