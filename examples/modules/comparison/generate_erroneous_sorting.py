"""
This generate a erroneous sorting to illustrate in some example
some possible mistake catch in ground truth comparison.

"""

import numpy as np
import matplotlib.pyplot as plt

import spikeinterface.extractors as se
import spikeinterface.sorters as sorters
import spikeinterface.comparison as sc
import spikeinterface.widgets as sw

def generate_erroneous_sorting():
    rec, sorting_true = se.example_datasets.toy_example(num_channels=4, duration=10, seed=10)
    
    sorting_err = se.NumpySortingExtractor()
    sorting_err.set_sampling_frequency(sorting_true.get_sampling_frequency())
    
    # sorting_true have 10 units
    np.random.seed(0)
    
    # unit 1 2 are perfect
    for u in [1, 2]:
        st = sorting_true.get_unit_spike_train(u)
        sorting_err.add_unit(u, st)

    # unit 3 4 (medium) 10 (low) have medium to low agreement
    for u, score in [(3, 0.8),  (4, 0.75), (10, 0.3)]:
        st = sorting_true.get_unit_spike_train(u)
        st = np.sort(np.random.choice(st, size=int(st.size*score), replace=False))
        sorting_err.add_unit(u, st)
    
    # unit 5 6 are over merge
    st5 = sorting_true.get_unit_spike_train(5)
    st6 = sorting_true.get_unit_spike_train(6)
    st = np.unique(np.concatenate([st5, st6]))
    st = np.sort(np.random.choice(st, size=int(st.size*0.7), replace=False))
    sorting_err.add_unit(56, st)
    
    # unit 7 is over split in 2 part
    st7 = sorting_true.get_unit_spike_train(7)
    st70 = st7[::2]
    sorting_err.add_unit(70, st70)
    st71 = st7[1::2]
    st71 = np.sort(np.random.choice(st71, size=int(st71.size*0.9), replace=False))
    sorting_err.add_unit(71, st71)
    
    # unit 8 is redundant 3 times
    st8 = sorting_true.get_unit_spike_train(8)
    st80 = np.sort(np.random.choice(st8, size=int(st8.size*0.65), replace=False))
    st81 = np.sort(np.random.choice(st8, size=int(st8.size*0.6), replace=False))
    st82 = np.sort(np.random.choice(st8, size=int(st8.size*0.55), replace=False))
    sorting_err.add_unit(80, st80)
    sorting_err.add_unit(81, st81)
    sorting_err.add_unit(82, st82)
    
    # unit 9 is missing
    
    # there are some units that do not exist 15 16 and 17
    nframes = rec.get_num_frames()
    for u in [15,16,17]:
        st = np.random.randint(0, high=nframes, size=35)
        sorting_err.add_unit(u, st)
        
    
    
    return sorting_true, sorting_err
    


    
if __name__ == '__main__':
    # just for check
    sorting_true, sorting_err = generate_erroneous_sorting()
    comp = sc.compare_sorter_to_ground_truth(sorting_true, sorting_err, exhaustive_gt=True)
    sw.plot_agreement_matrix(comp, ordered=True)
    plt.show()

