#@title <b>Bulanık Kümeleme Algoritmaları ve Geçerlilik Indexleri</b>
"""
Author: Fatih KUTLU, İbrahim AYAZ
Created Date: 01.01.2021
Updated Date: 23.01.2021
Version:0.5
"""

import numpy as np
import time



class FCM:
    """
    Fuzzy C Means (Bulanık C Ortalamalar)
    """
    def __init__(self, c, m, eps, maxIter, data):
        """
        Parameters
        ----------
        c : int
            Küme Sayısı
        m : float
            Bulanıklaştırıcı 1<=m
        eps : float
            Epsilon (Durdurma Kriteri) 0<eps<1
        maxIter : int
            Maksimum İterasyon Sayısı
        data : array
            Veri Seti

        -------

        """
        self.c = c
        self.m = m
        self.eps = eps
        self.maxIter = maxIter
        self.data = data

    def BaslangicMatrisini_Olustur(self):
        U = np.random.randint(100, 200, size=(len(self.data), self.c))
        return U/U.sum(axis=1, keepdims=True)

    def V(self, U):
        U_m = U**self.m
        U_m = U_m/U_m.sum(axis=0, keepdims=True)
        return np.matmul(U_m.T, self.data)

    def U(self, V_eski):
        U_yeni = np.zeros(shape=(self.data.shape[0], self.c))
        for i in range(U_yeni.shape[0]):
            for j in range(U_yeni.shape[1]):
                U_yeni[i][j] = 1./np.linalg.norm(self.data[i]-V_eski[j])

        U_yeni = U_yeni**(2./(self.m-1))
        U_yeni = U_yeni/U_yeni.sum(axis=1, keepdims=True)
        return U_yeni

    def SSE(self, U, V):
        U_m = U**self.m
        toplam_karesel_hata = 0
        for j in range(self.c):
            for i in range(self.data.shape[0]):
                toplam_karesel_hata += U_m[i][j] * np.linalg.norm(self.data[i]-V[j])**2
        return toplam_karesel_hata

    def Kumele(self):
        baslangic_zamani = time.time()
        U = self.BaslangicMatrisini_Olustur()
        print("INFO: Başlangıç matrisi oluşturuldu.")
        V = np.zeros((self.c, self.data.shape[0]))
        hata = float(self.SSE(U, V))
        iterasyon = 1
        loss_degerleri = []
        while iterasyon <= self.maxIter:
            V = self.V(U)
            U = self.U(V)
            hata_yeni = float(self.SSE(U, V))
            loss = hata - hata_yeni
            loss_degerleri.append(loss)
            print(str(iterasyon) + ". iterasyon - Loss: " + str(loss))
            iterasyon += 1
            if loss < self.eps:
                break
            hata = hata_yeni
        bitis_zamani = time.time()
        toplam_gecen_saniye = bitis_zamani-baslangic_zamani
        toplam_dakika = toplam_gecen_saniye/60
        print("INFO: Kümeleme işlemi " + str(toplam_dakika) + " dakikada tamamlandı.")
        return U, V, loss_degerleri

class IFCM:
    """
    Intuitionistic Fuzzy C Means (Sezgisel Bulanık C Ortalamalar)
    """

    def __init__(self, c, m, eps, maxIter, data, lam=2):
        """
          Parameters
          ----------
          c : int
              Küme Sayısı
          m : float
              Bulanıklaştırıcı 1<=m
          eps : float
              Epsilon (Durdurma Kriteri) 0<eps<1
          maxIter : int
              Maksimum iterasyon sayısı
          lam : float
              Üye olmama derecesindeki lambda değeridir ve varsayılan değeri 2'dir.
          data : array
              Veri Seti.

          -------

        """
        self.c = c
        self.m = m
        self.eps = eps
        self.maxIter = maxIter
        self.data = data
        self.lam = lam

    def BaslangicMatrisini_Olustur(self):
        U = np.random.randint(100, 200, size=(len(self.data), self.c))
        return U/U.sum(axis=1, keepdims=True)

    def U(self, Z, V):
        U_yeni = np.zeros(shape=(self.data.shape[0], self.c))
        for i in range(U_yeni.shape[0]):
            for j in range(U_yeni.shape[1]):
                U_yeni[i][j] = 1./self.Uzaklik(Z[i], V[j])

        U_yeni = U_yeni**(2./(self.m-1))
        U_yeni = U_yeni/U_yeni.sum(axis=1, keepdims=True)
        return U_yeni

    def V(self, U, u_z, n_z, p_z):
        U_m = U**self.m
        U_m = U_m/U_m.sum(axis=0, keepdims=True)
        u_v=np.matmul(U_m.T, u_z)
        n_v=np.matmul(U_m.T, n_z)
        p_v=np.matmul(U_m.T, p_z)

        v=zip(u_v, n_v, p_v)

        return list(v)
        
    def Z(self, data):
        u=self.Z_UyeOlmaDerecesi(data)
        n=self.Z_UyeOlmamaDerecesi(u)
        p=self.Z_BelirsizlikDerecesi(u,n)
        z=zip(u,n,p)
        return list(z), u, n, p

    def Z_UyeOlmaDerecesi(self, data):
        buyuk=np.max(data)
        kucuk=np.min(data)
        u=[]
        for x in data:
            u.append((x-kucuk)/(buyuk-kucuk))
        return u

    def Z_UyeOlmamaDerecesi(self, U_z):
        n=[]
        for u in U_z:
            n.append((1-u)/(1+self.lam*u))
        return n

    def Z_BelirsizlikDerecesi(self, U_z, N_z):
        pi=[]
        for i in range(len(U_z)):
            pi.append(1-(U_z[i]+N_z[i]))
        return pi

    def Hata_Hesapla(self, V_eski, V_yeni):
        toplam=0
        for i in range(self.c):
            toplam+=self.Uzaklik(V_eski[i], V_yeni[i])
        return toplam/self.c

    def Uzaklik(self, Z, V, W=1):
        toplam=((Z[0]-V[0])**2 + (Z[1]-V[1])**2 + (Z[2]-V[2])**2)
        return W * np.sqrt(toplam)

    def Kumele(self):
        baslangic_zamani=time.time()
        U = self.BaslangicMatrisini_Olustur()
        print("INFO: Başlangıç matrisi oluşturuldu.")
        V = [(0,0,0) for i in range(self.c)]
        iterasyon=1
        Z,u_z,n_z,p_z=self.Z(self.data)
        loss_degerleri=[]
        while iterasyon<=self.maxIter:          
            v_eski=V
            V=self.V(U, u_z, n_z, p_z)
            U=self.U(Z,V)
            v_yeni=V
            loss=self.Hata_Hesapla(v_eski, v_yeni)
            print(str(iterasyon)+". iterasyon - Loss: "+ str(loss))
            loss_degerleri.append(loss)
            if (loss<self.eps):
                break
            iterasyon+=1
        bitis_zamani=time.time()
        toplam_gecen_saniye=bitis_zamani-baslangic_zamani
        toplam_dakika=toplam_gecen_saniye/60
        print("INFO: Kümeleme işlemi "+ str(toplam_dakika) +" dakikada tamamlandı.")
        return U, V, loss_degerleri

class CVIndex:
    """
    Cluster Validity Index (Küme Geçerlilik İndeksi)
    """

    def __init__(self, u, v,m, data):
        self.u=u
        self.v=v
        self.m=m
        self.data=data

    
    def PC(self):
        """
        Partition Coefficient (Bölünme Kat Sayısı)    
        """
        return (self.u**2).sum()/len(self.data)
    

    def CE(self):
        """
        Classification Entropy (Sınıflandırma Entropisi)
        """
        return (self.u*np.log(self.u)).sum()/-len(self.data)
    
    def MPC(self):
        """
        Modificated Partititon Coefficient (Gözden geçirilmiş Bölünme Katsayısı)\n
        Normalized Partititon Coefficient (Normalleştirilmiş Bölünme Katsayısı)
        """
        c=self.u.shape[1]
        return 1-(c/(c-1))*(1-PC())
    
    def XB(self):
        """
        Xie-Beni Index kodları buraya gelecek
        """
        pass