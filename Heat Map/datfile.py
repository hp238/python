import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
import os
import numpy as np

class DatFile:
    
    data_type=dict()
    data_type[8]="int8"
    data_type[16]="int16"
    data_type[32]="int32"
    data_type[64]="int64"
    
     
    def __init__(self,dpath=None, num_channels=None, bit_per_sample=None, sample_rate=None,):
        
        if (dpath is not None) and (num_channels is not None) and (bit_per_sample is not None) and (sample_rate is not None):

            self.filename = dpath
            self.num_channels = num_channels
            self.bit_per_sample = bit_per_sample # Checar se é válido !!
            # if not (bit_per_sample in data_type.keys()) ---> Gerar ERRO
            self.sample_rate = sample_rate
            statinfo = os.stat(dpath) # Vulnerável
            self.filesize = statinfo.st_size
            self.data = self.loadfile() # Q1
            self.data = self.data.T
            
            
        else:
            self.filename=None
            self.num_channels=None
            self.bit_per_sample=None
            self.sample_rate=None
            self.filesize = None
            self.data = None
            print ("The object is empty.. Please revise your input parameters")  
    def get_filename(self):
        return (self.filename)
    
    def get_num_channels(self):
        return (self.num_channels)
    
    def get_bit_per_sample(self):
        return (self.bit_per_sample)
    
    def get_sample_rate(self):
        return (self.sample_rate)
    
    def show_status(self):
        print ("Filename: ",self.get_filename())
        print ("Number of channels: ",self.get_num_channels())
        print ("bit per sample: ",self.get_bit_per_sample())
        print ("Sammpling rate (Hz): ",self.get_sample_rate())
        
    def get_filesize(self):
        return (self.filesize)
        
    def loadfile (self):
        # Vulnerário
        if (dpath is None):
            return (None)
        pop_sample_size_in_bytes = self.num_channels*self.bit_per_sample/8;
        num_sampling_periods = int(self.filesize/pop_sample_size_in_bytes)
        mem_map_data = np.memmap(dpath, dtype="int16", shape=(num_sampling_periods, self.num_channels))
        return (mem_map_data)
    
    def duration(self): #Q3
        # Vulnerável !!
        pop_sample_size_in_bytes = self.num_channels*self.bit_per_sample/8;
        num_sampling_periods = int(self.filesize/pop_sample_size_in_bytes)
        return (num_sampling_periods/self.sample_rate)
    
    def plot_channel(self,ch,t1,t2,ax):
        i1=np.floor(t1*self.sample_rate)
        i2=np.floor(t2*self.sample_rate)
        #print (t1,t2,i1,i2)
        #type (ax)
        ax.plot(self.data[ch,i1:i2])
        
    
    def crop (self,t1,t2,channel_list=None):
        ''' Retorna em uma matriz uma parte do conteúdo do dat file.
        Entradas:
        * t1: instante de tempo inicial, em segundos
        * t2: instante de tempo final, em segundos
        * channel_list: lista de canais a serem incluı́dos. Por default,
        todos os canais serão incluı́dos.
        Saı́da: Uma numpy matrix com o conteúdo parcial do dat file, conforme
        os parâmetros de entrada ou None se houve algum problema na execução
        '''
        col1=np.floor(t1*self.sample_rate)
        col2=np.floor(t2*self.sample_rate)
        if (channel_list is None):
            return (df.data[:,col1:col2]) # Vulnerável: validar col1 e col2
        else:
            channel_list.sort
            return (df.data[channel_list,col1:col2]) # Validar channel_list
                   
    def subsample (self,fileout,k,channel_list=None,overwrite=False):
            ''' Salva uma versão ao subamostrada do conteúdo do dat file em dado
            arquivo de saı́da.
            Entradas:
                * fileout: caminho completo para o arquivo de saı́da
                * k: fator (inteiro) de subamostragem;
                * channel_list: lista de canais a serem incluı́dos. Por default,
                    todos os canais serão ao incluı́dos.'''
            # Validar o fileout
            if (channel_list is not None):
                np.save(fileout,self.data[:,::k]) # Validar o k
            else:
                channel_list.sort
                np.save(fileout,self.data[channel_list,::k]) # Validar o k # Validar channel_list


    def hpfilter (self,t1,t2,channel_list=None,l_freq=300,h_freq=1200,butter_order=3): 
        return
