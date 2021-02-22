from klusta.kwik import KwikModel
import numpy as np
import pandas as pd


class KwikFile:
    """!  @brief Model for Kwik file, strongly based on KwikModel from phy project

    The main purpose of this class is provide an abstraction for kwik files provided by phy project. The current version contains a basic set of fundamental methods used in kwik file      
    @author: Nivaldo A P de Vasconcelos
    @date: 2018.Feb.02
    """
    
    #get_path
    def __init__(self,kpath=None,name=None):
        
        
        self.kwik_model=None
        self.name = name
        self.kpath=None
        if (kpath is not None):
            self.kwik_model=KwikModel(kpath)
            self.kpath=kpath
            if (name is None):
                self.name = self.kwik_model.name
            print ("Created class on = %s !" % kpath)
        else:
            print ("It still with no path:(")
    


    def get_name(self):
        """! @brief Returns the found in name field in kwik file.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        return (self.name)

    def set_kwik_file (self,kpath):
        """! @brief Defines the corresponding kwik file

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        self.kwik_model=KwikModel(kpath)
        self.name = self.kwik_model.name
        self.kpath=kpath


    def sampling_rate (self):
        """! @brief Returns the sampling rate used during the recordings 

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        return (self.kwik_model.sample_rate)
    
    def shank (self):
        """! @brief Returns the shank/population's id used to group the recordings.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        return (self.kwik_model.name)
    
    def get_spike_samples (self):
        """! @brief Returns the spike's samples on the recordings.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """

        return (self.kwik_model.spike_samples)
    
    def get_spike_clusters (self):
        """! @brief Returns the corresponding spike's clusters on the recordings.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        return (self.kwik_model.spike_clusters)
    
    def describe(self):
        """! @brief Describes the kwik file

        It calls the describe method in KwikModel

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        self.kwik_model.describe()

    def close (self):
        """! @brief Closes the corresponding kwik model

        It calls the close method in KwikModel

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        self.kwik_model.close()

    def list_of_groups (self):
        """! @brief Returns the list of groups found in kwik file

        The result has a list's form.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """

        lgroups = list(self.groups().values())
        lgroups = list(set(lgroups))

        return (lgroups)

    def list_of_non_noisy_groups (self):

        """! @brief Returns the list of groups found in kwik file which are not called noise

        The result has a list's form.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """

        lgroups = list(self.groups().values())
        lgroups = list(set(lgroups)-set(['noise',]))
        return (lgroups)


    def all_clusters (self):
        """! @brief Returns the list of all clusters in kwik file

        The result has a list's form.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """

        llabels = list(self.groups().keys())
        llabels = list(set(llabels))

        return (llabels)


    def groups(self):
        """! @brief Returns a dict with cluster label and its respective group

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        if not(isinstance(self.kwik_model,KwikModel)):
            raise ValueError("There is no KwikModel assigned for this object.")
        return (self.kwik_model.cluster_groups)


    def clusters (self,group_name=None):
        """! @brief Returns the list of clusters on kwik file

        It can be used to get the list of clusters for a given group by pproviding
        this information the group_name.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02
        """
        if (group_name is None):
            return (self.all_clusters())
 
        if not(group_name in self.list_of_groups()):
            raise ValueError("\nThis group was not found in kwik file: %s\n" % group_name)
        group=self.groups()

        clusters=[]
        for c in self.all_clusters():
            if (group[c]==group_name):
                clusters.append(c)
        clusters.sort()
        return (clusters)

    def all_spikes_on_groups (self,group_names):
        """! @brief Returns the all spike samples within a list of groups

        Usually the clusters are organized in groups. Ex: noise, mua, sua,
        unsorted This method returns, in a single list of spike samples, all
        spikes found in a lists of groups (group_names). 

        Parameters:
        group_names: list of group names, where the spikes will be searched. 

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02 
        """

        spikes=[]
        all_spikes=self.get_spike_samples()
        all_labels=self.get_spike_clusters()
        
        if not(isinstance(group_names,list)):
           raise ValueError("\nThe argument must be a list.") 
        
        for group_name in group_names:
            if not(group_name in self.list_of_groups()):
                raise ValueError("\nThis group was not found in kwik file: %s\n" % group_name)
            for c in self.clusters(group_name=group_name):
                spikes=spikes+list(all_spikes[all_labels==c])
        spikes.sort()
        return (spikes)

    def all_spike_id_on_groups (self,group_names):
        """! @brief Returns the all spike id within a list of groups

        Usually the clusters are organized in groups. Ex: noise, mua, sua,
        unsorted This method returns, in a single list of spike samples, all
        spikes found in a lists of groups (group_names). 

        Parameters:
        group_names: list of group names, where the spike ids will be searched. 

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Jun.05
        """

        spk_id=[]
        all_spk_id=self.kwik_model.spike_ids
        all_labels=self.get_spike_clusters()
        
        if not(isinstance(group_names,list)):
           raise ValueError("\nThe argument must be a list.") 
        
        for group_name in group_names:
            if not(group_name in self.list_of_groups()):
                raise ValueError("\nThis group was not found in kwik file: %s\n" % group_name)
            for c in self.clusters(group_name=group_name):
                spk_id=spk_id+list(all_spk_id[all_labels==c])
        spk_id.sort()
        return (spk_id)
    
    def all_spike_id_on_cluster(self,cluster_id):
        
        if not(cluster_id in self.all_clusters()):
            raise ValueError("\nThis cluster was not found in kwik file: %s\n" % cluster_id)
        all_spk_id=self.kwik_model.spike_ids
        all_labels=self.get_spike_clusters()
        spk_id=list(all_spk_id[all_labels==cluster_id])
        spk_id.sort()
        return (spk_id)
    
    def group_firing_rate (self,group_names=None,a=None,b=None): 
        """! @brief Returns firing rate in a given set of groups found in kwik file.

        Usually, the clusters are organized in groups. Ex: noise, mua, sua,
        unsorted. This method returns, in a doubled dictionary, the firing rate
        for each cluster, organized by groups.

        Parameters: 
        group_names: list of group names, where the spikes will be
        searched. When this input is 'None' all groups are taken. The resulting
        dictionary has the first keys as groups, and the second keys as the
        respective cluster id's, whereas the value, is the corresponding firing
        rate within [a,b].


        Please refer to the method cluster_firing_rate in order to get more 
        details about the firing calculation.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02 
        """
        if not(isinstance(group_names,list)) and not(group_names is None):
           raise ValueError("\nThe argument must be a list or a None.") 
        spk=dict()
        if group_names is None:
            group_names=self.list_of_non_noisy_groups()
        for group_name in group_names:
            if not(group_name in self.list_of_groups()):
                raise ValueError("\nThis group was not found in kwik file: %s\n" % group_name)
            spk[group_name]=dict()
            for c in self.clusters(group_name=group_name):
                spk[group_name][c]=self.cluster_firing_rate(c,a=a,b=b)
        return (spk)


    def cluster_firing_rate (self,cluster_id,a=None,b=None):
        """! @brief Returns firing rate in a given cluster_id found in the kwik file

        In the kwik file, a cluster stores the spike times sorted for a given neuronal
        unit. The firing rate here is calculated by dividing the number of spike times
        by the number of seconds of the time period definedd by [a,b]. 
        If a is 'None' a is assingned to zero; if b is 'None', it is assigned to the time
        of the last spike within the cluster.

        Parameters:
        cluster_id: id which identifies the cluster.
        a,b: limits of the time period where the firing rate must be calculated.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02 
        """
        sr=self.sampling_rate()
        spikes=np.array(self.spikes_on_cluster (cluster_id))/sr
        if a is None:
            a=0
        if b is None:
            b=spikes[-1]
        if (a==b):
            raise ValueError ("\nThe limits of the time interval are equal\n")
        piece=spikes[(spikes>=a)]
        piece=piece[piece<=b]
        return (len(piece)/(b-a))

    def spikes_on_cluster (self,cluster_id):
        """! @brief Returns the all spike samples within a single cluster

        Parameters:
        cluster_id: id used to indentify the cluster.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02 
        """

        if not(cluster_id in self.all_clusters()):
            raise ValueError("\nThis cluster was not found in kwik file: %s\n" % cluster_id)
        all_spikes=self.get_spike_samples()
        all_labels=self.get_spike_clusters()
        spikes=list(all_spikes[all_labels==cluster_id])
        spikes.sort()
        return (spikes)

    def group_firing_rate_to_dataframe (self,group_names=None,a=None,b=None):
        """! @brief Exports the group's firing rate into a pandas dataframe


        Usually, the clusters are organized in groups. Ex: noise, mua, sua,
        unsorted. This method returns, in a pandas dataframe, which contains the
        following information for each unit: 'shank', 'group', 'label', and 'fr';

        
        Parameters:
        group_names: list of group names, where the spikes will be
        searched. When this input is 'None' all groups are taken. The resulting
        dictionary has the first keys as groups, and the second keys as the
        respective cluster id's, whereas the value, is the corresponding firing
        rate within [a,b].

        Please refer to the method cluster_firing_rate in order to get more 
        details about the firing calculation.

        Author: Nivaldo A P de Vasconcelos
        Date: 2018.Feb.02 
        """
        d=self.group_firing_rate (group_names=group_names,a=a,b=b)

        shank_id = self.name
        group_names = d.keys()
        data=[]
        for group_name in group_names:
            for label in d[group_name].keys():        
                fr=d[group_name][label]
                data.append ({"shank_id":shank_id, "group":group_name,"label":label,"fr":fr})
        return (pd.DataFrame(data))










        




