import numpy as np
from scipy.integrate import quad
from .boys import *

def phi_n_unnorm(t,n,alphaa,beta,X):
    if(n==0):
        return 1
    elif(n>0):
        return (t*phi_n(t,n-1,alphaa,beta,X)-beta[n-1]*phi_n(t,n-2,alphaa,beta,X)-alphaa[n-1]*phi_n(t,n-1,alphaa,beta,X))
    else:
        return 0

def phi_n(t,n,alphaa,beta,X):
    if(n==0):
        return 1/np.sqrt(F_n(0,X))
    elif(n>0):
        return (t*phi_n(t,n-1,alphaa,beta,X)-beta[n-1]*phi_n(t,n-2,alphaa,beta,X)-alphaa[n-1]*phi_n(t,n-1,alphaa,beta,X))/beta[n]
    else:
        return 0
    
def alphaa_func(t,n,alphaa,beta,X):
    return phi_n(t**2,n,alphaa,beta,X)*t**2*phi_n(t**2,n,alphaa,beta,X)*np.exp(-X*t**2)

def beta_func(t,n,alphaa,beta,X):
    return phi_n_unnorm(t**2,n,alphaa,beta,X)*phi_n_unnorm(t**2,n,alphaa,beta,X)*np.exp(-X*t**2)

def get_weights_roots(points,X):

    alphaa = np.zeros(points)
    beta = np.zeros(points)

    for n in range(points):
        beta[n] = np.sqrt(quad(beta_func,0,1,args=(n,alphaa,beta,X))[0])
        alphaa[n] = quad(alphaa_func,0,1,args=(n,alphaa,beta,X))[0]

    M = np.zeros((points,points))
    for i in range(points):
        M[i][i] = alphaa[i]
        if(i>0):
            M[i][i-1] = beta[i]
        if(i<points-1):
            M[i][i+1] = beta[i+1]     
            
    val,vec = np.linalg.eigh(M)
    w = np.zeros(points)
    for i in range(points):
        w[i] = vec[0][i]**2*F_n(0,X)
    roots = np.sqrt(val)
    return w,roots


# ## DKR4

# Se define la relación de recurrencia
# \begin{eqnarray}
# I_{i+1,j,k,l} &=& \left( X_{PA} - \frac{\alpha}{p}X_{PQ}s^2 \right) I_{ijkl} + \frac{1}{2p} \left(1-\frac{\alpha}{p} s^2 \right) (iI_{i-1,j,k,l} + jI_{i,j-1,k,l}) + \frac{s^2}{2(p+q)}(kI_{i,j,k-1,l}+lI_{i,j,k,l-1})\\
# I_{i,j,k+1,l} &=& \left( X_{QC} + \frac{\alpha}{q}X_{PQ}s^2 \right) I_{ijkl} + \frac{1}{2q} \left(1-\frac{\alpha}{q} s^2 \right) (kI_{i,j,k-1,l} + lI_{i,j,k,l-1}) + \frac{s^2}{2(p+q)}(iI_{i-1,j,k,l}+jI_{i,j-1,k,l})
# \end{eqnarray}

def I_DKR4(s,i,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz):    

    if(i<0 or j<0 or k<0 or l<0):
        return 0
    elif(i>0):
        return ((pairAB.coord[ii][xyz]-pairAB.g_a.coord[xyz])-alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*s**2)*I_DKR4(s,i-1,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz) + 1/(2*pairAB.exp[ii])*(1-alpha/pairAB.exp[ii]*s**2)*((i-1)*I_DKR4(s,i-2,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz)+j*I_DKR4(s,i-1,j-1,k,l,pairAB,pairCD,alpha,ii,jj,xyz)) + s**2/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(k*I_DKR4(s,i-1,j,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz) + l*I_DKR4(s,i-1,j,k,l-1,pairAB,pairCD,alpha,ii,jj,xyz))
    elif(j>0):
        return ((pairAB.coord[ii][xyz]-pairAB.g_b.coord[xyz])-alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*s**2)*I_DKR4(s,i,j-1,k,l,pairAB,pairCD,alpha,ii,jj,xyz) + 1/(2*pairAB.exp[ii])*(1-alpha/pairAB.exp[ii]*s**2)*((j-1)*I_DKR4(s,i,j-2,k,l,pairAB,pairCD,alpha,ii,jj,xyz)+i*I_DKR4(s,i-1,j-1,k,l,pairAB,pairCD,alpha,ii,jj,xyz)) + s**2/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(k*I_DKR4(s,i,j-1,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz) + l*I_DKR4(s,i,j-1,k,l-1,pairAB,pairCD,alpha,ii,jj,xyz))
    elif(k>0):
        return ((pairCD.coord[jj][xyz]-pairCD.g_a.coord[xyz])+alpha/pairCD.exp[jj]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*s**2)*I_DKR4(s,i,j,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz) + 1/(2*pairCD.exp[jj])*(1-alpha/pairCD.exp[jj]*s**2)*((k-1)*I_DKR4(s,i,j,k-2,l,pairAB,pairCD,alpha,ii,jj,xyz)+l*I_DKR4(s,i,j,k-1,l-1,pairAB,pairCD,alpha,ii,jj,xyz)) + s**2/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(i*I_DKR4(s,i-1,j,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz) + j*I_DKR4(s,i,j-1,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz))
    elif(l>0):
        return ((pairCD.coord[jj][xyz]-pairCD.g_b.coord[xyz])+alpha/pairCD.exp[jj]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*s**2)*I_DKR4(s,i,j,k,l-1,pairAB,pairCD,alpha,ii,jj,xyz) + 1/(2*pairCD.exp[jj])*(1-alpha/pairCD.exp[jj]*s**2)*((l-1)*I_DKR4(s,i,j,k,l-2,pairAB,pairCD,alpha,ii,jj,xyz)+k*I_DKR4(s,i,j,k-1,l-1,pairAB,pairCD,alpha,ii,jj,xyz)) + s**2/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*(i*I_DKR4(s,i-1,j,k,l-1,pairAB,pairCD,alpha,ii,jj,xyz) + j*I_DKR4(s,i,j-1,k,l-1,pairAB,pairCD,alpha,ii,jj,xyz))
    else:
        return np.exp(-pairAB.alpha[ii]*(pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])**2)*np.exp(-pairCD.alpha[jj]*(pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])**2)


# Finalmente
# \begin{equation}
# g_{abcd} = \frac{2\pi^{5/2}}{pq\sqrt{p+q}} \sum_{k=1}^\gamma w_k I_x(s_k^2) I_y(s_k^2) I_z(s_k^2)
# \end{equation}

def DKR4(pairAB,pairCD):

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
                        aux2 = 0.0
                        for jj in range(pairCD.k):
                            
                            alpha = pairAB.exp[ii]*pairCD.exp[jj]/(pairAB.exp[ii]+pairCD.exp[jj])
                            Rpq = np.linalg.norm(pairAB.coord[ii]-pairCD.coord[jj])
                    
                            points = int((lax+lay+laz+lbx+lby+lbz+lcx+lcy+lcz+ldx+ldy+ldz)/2)+1
                            w,s = get_weights_roots(points,alpha*Rpq**2)
                            
                            aux1 = 0
                            for k in range(points):
                                aux1 += w[k]*I_DKR4(s[k],lax,lbx,lcx,ldx,pairAB,pairCD,alpha,ii,jj,0)*I_DKR4(s[k],lay,lby,lcy,ldy,pairAB,pairCD,alpha,ii,jj,1)*I_DKR4(s[k],laz,lbz,lcz,ldz,pairAB,pairCD,alpha,ii,jj,2)
                            aux1 = 2*np.pi**(5/2)/(pairAB.exp[ii]*pairCD.exp[jj]*np.sqrt(pairAB.exp[ii]+pairCD.exp[jj]))*aux1                            
                            aux2 += aux1*pairCD.coef[jj]
                        integral += aux2*pairAB.coef[ii]
                        
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result    
                


# ## DKR2

# Se define la relación de recurrencia
# \begin{eqnarray}
# I_{i+1,0,k,0} &=& \left( X_{PA} - \frac{\alpha}{p}X_{PQ}s^2 \right) I_{i0k0} + \frac{1}{2p} \left(1-\frac{\alpha}{p} s^2 \right) (iI_{i-1,0,k,0}) + \frac{s^2}{2(p+q)}(kI_{i,j,k-1,l})\\
# I_{i,0,k+1,0} &=& \left( X_{QC} + \frac{\alpha}{q}X_{PQ}s^2 \right) I_{i0k0} + \frac{1}{2q} \left(1-\frac{\alpha}{q} s^2 \right) (kI_{i,0,k-1,0}) + \frac{s^2}{2(p+q)}(iI_{i-1,j,k,l})
# \end{eqnarray}

def I_DKR2(s,i,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz):    

    if(i<0 or j<0 or k<0 or l<0):
        return 0
    elif(i>0):
        return ((pairAB.coord[ii][xyz]-pairAB.g_a.coord[xyz])-alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*s**2)*I_DKR2(s,i-1,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz) + 1/(2*pairAB.exp[ii])*(1-alpha/pairAB.exp[ii]*s**2)*(i-1)*I_DKR2(s,i-2,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz) + s**2/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*k*I_DKR2(s,i-1,j,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz)
    elif(k>0):
        return ((pairCD.coord[jj][xyz]-pairCD.g_a.coord[xyz])+alpha/pairCD.exp[jj]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*s**2)*I_DKR2(s,i,j,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz) + 1/(2*pairCD.exp[jj])*(1-alpha/pairCD.exp[jj]*s**2)*(k-1)*I_DKR2(s,i,j,k-2,l,pairAB,pairCD,alpha,ii,jj,xyz) + s**2/(2*(pairAB.exp[ii]+pairCD.exp[jj]))*i*I_DKR2(s,i-1,j,k-1,l,pairAB,pairCD,alpha,ii,jj,xyz)
    else:
        return np.exp(-pairAB.alpha[ii]*(pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])**2)*np.exp(-pairCD.alpha[jj]*(pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])**2)


# Se añade relación de recurrencia horizontal

def HRR_DKR2(pairAB,pairCD,i,j,k,l,N):

    for xyz in range(3):
        if(l[xyz]!=0):
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            kp1 = k[:]
            kp1[xyz] = kp1[xyz] + 1
            return HRR_DKR2(pairAB,pairCD,i,j,kp1,lm1,N) + (pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])*HRR_DKR2(pairAB,pairCD,i,j,k,lm1,N)
        elif(j[xyz]!=0):
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            ip1 = i[:]
            ip1[xyz] = ip1[xyz] + 1
            return HRR_DKR2(pairAB,pairCD,ip1,jm1,k,l,N) + (pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])*HRR_DKR2(pairAB,pairCD,i,jm1,k,l,N)
    
    integral = 0.0
    for ii in range(pairAB.k):
        aux2 = 0.0
        for jj in range(pairCD.k):
                    
            alpha = pairAB.exp[ii]*pairCD.exp[jj]/(pairAB.exp[ii]+pairCD.exp[jj])
            Rpq = np.linalg.norm(pairAB.coord[ii]-pairCD.coord[jj])
                
            points = int((i[0]+i[1]+i[2]+j[0]+j[1]+j[2]+k[0]+k[1]+k[2]+l[0]+l[1]+l[2])/2)+1
            w,s = get_weights_roots(points,alpha*Rpq**2)
                        
            aux1 = 0
            for kk in range(points):
                aux1 += w[kk]*I_DKR2(s[kk],i[0],j[0],k[0],l[0],pairAB,pairCD,alpha,ii,jj,0)*I_DKR2(s[kk],i[1],j[1],k[1],l[1],pairAB,pairCD,alpha,ii,jj,1)*I_DKR2(s[kk],i[2],j[2],k[2],l[2],pairAB,pairCD,alpha,ii,jj,2)
            aux1 = 2*np.pi**(5/2)/(pairAB.exp[ii]*pairCD.exp[jj]*np.sqrt(pairAB.exp[ii]+pairCD.exp[jj]))*aux1                            
            aux2 += aux1*pairCD.coef[jj]
        integral += aux2*pairAB.coef[ii]
    
    return integral


def DKR2(pairAB,pairCD):

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
                    integral = HRR_DKR2(pairAB,pairCD,i,j,k,l,0)                
                    
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result           

# ## DKR1

# Se define la relación de recurrencia
# \begin{eqnarray}
# I_{i+1,0,0,0} &=& \left( X_{PA} - \frac{\alpha}{p}X_{PQ}s^2 \right) I_{i000} + \frac{1}{2p} \left(1-\frac{\alpha}{p} s^2 \right) (iI_{i-1,0,0,0})\\
# \end{eqnarray}

def I_DKR1(s,i,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz):    

    if(i<0 or j<0 or k<0 or l<0):
        return 0
    elif(i>0):
        return ((pairAB.coord[ii][xyz]-pairAB.g_a.coord[xyz])-alpha/pairAB.exp[ii]*(pairAB.coord[ii][xyz]-pairCD.coord[jj][xyz])*s**2)*I_DKR1(s,i-1,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz) + 1/(2*pairAB.exp[ii])*(1-alpha/pairAB.exp[ii]*s**2)*(i-1)*I_DKR1(s,i-2,j,k,l,pairAB,pairCD,alpha,ii,jj,xyz)
    else:
        return np.exp(-pairAB.alpha[ii]*(pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])**2)*np.exp(-pairCD.alpha[jj]*(pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])**2)

def trans_elec_DKR1(i,j,k,l,pairAB,pairCD,ii,jj):
    
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
            return -(pairAB.ab[ii][1]*(pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])+pairCD.ab[jj][1]*(pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz]))/pairCD.exp[jj]*trans_elec_DKR1(i,j,km1,l,pairAB,pairCD,ii,jj) + i[xyz]/(2*pairCD.exp[jj])*trans_elec_DKR1(im1,j,km1,l,pairAB,pairCD,ii,jj) + (k[xyz]-1)/(2*pairCD.exp[jj])*trans_elec_DKR1(i,j,km2,l,pairAB,pairCD,ii,jj) - pairAB.exp[ii]/pairCD.exp[jj]*trans_elec_DKR1(ip1,j,km1,l,pairAB,pairCD,ii,jj)
                
    alpha = pairAB.exp[ii]*pairCD.exp[jj]/(pairAB.exp[ii]+pairCD.exp[jj])
    Rpq = np.linalg.norm(pairAB.coord[ii]-pairCD.coord[jj])
                
    points = int((i[0]+i[1]+i[2]+j[0]+j[1]+j[2]+k[0]+k[1]+k[2]+l[0]+l[1]+l[2])/2)+1
    w,s = get_weights_roots(points,alpha*Rpq**2)
                        
    integral = 0
    for kk in range(points):
        integral += w[kk]*I_DKR1(s[kk],i[0],j[0],k[0],l[0],pairAB,pairCD,alpha,ii,jj,0)*I_DKR1(s[kk],i[1],j[1],k[1],l[1],pairAB,pairCD,alpha,ii,jj,1)*I_DKR1(s[kk],i[2],j[2],k[2],l[2],pairAB,pairCD,alpha,ii,jj,2)
    integral = 2*np.pi**(5/2)/(pairAB.exp[ii]*pairCD.exp[jj]*np.sqrt(pairAB.exp[ii]+pairCD.exp[jj]))*integral   
    
    return integral

def HRR_DKR1(pairAB,pairCD,i,j,k,l):

    for xyz in range(3):
        if(l[xyz]!=0):
            lm1 = l[:]
            lm1[xyz] = lm1[xyz] - 1
            kp1 = k[:]
            kp1[xyz] = kp1[xyz] + 1
            return HRR_DKR1(pairAB,pairCD,i,j,kp1,lm1) + (pairCD.g_a.coord[xyz]-pairCD.g_b.coord[xyz])*HRR_DKR1(pairAB,pairCD,i,j,k,lm1)
        elif(j[xyz]!=0):
            jm1 = j[:]
            jm1[xyz] = jm1[xyz] - 1
            ip1 = i[:]
            ip1[xyz] = ip1[xyz] + 1
            return HRR_DKR1(pairAB,pairCD,ip1,jm1,k,l) + (pairAB.g_a.coord[xyz]-pairAB.g_b.coord[xyz])*HRR_DKR1(pairAB,pairCD,i,jm1,k,l)
    
    integral = 0.0
    for ii in range(pairAB.k):
        aux1 = 0.0
        for jj in range(pairCD.k):
            aux1 += trans_elec_DKR1(i,j,k,l,pairAB,pairCD,ii,jj)*pairCD.coef[jj]
        integral += aux1*pairAB.coef[ii]
    return integral

def DKR1(pairAB,pairCD):

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
                    integral = HRR_DKR1(pairAB,pairCD,i,j,k,l)                
                    
                    result[a][b][c][d] = g_a.N[a]*g_b.N[b]*g_c.N[c]*g_d.N[d]*integral
    return result
