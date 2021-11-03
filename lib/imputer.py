import tensorflow as tf
print('tf version', tf.__version__)
import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import Model
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.layers import Input,SpatialDropout1D, Embedding, LSTM, Dense, merge, Convolution2D, Lambda, GRU, TimeDistributed, Reshape, Permute, Convolution1D, Masking, Bidirectional
from keras.optimizers import Adam
from keras.layers import concatenate
from keras.regularizers import l2
from keras.callbacks import ModelCheckpoint
from keras import optimizers, callbacks
import numpy as np
import math
from keras.layers import Embedding, Add, concatenate, Input, Softmax
from keras import backend as K
#keras.activations.softmax(x, axis=-1)
from keras.activations import softmax

print('keras version', keras.__version__)

from keras.losses import binary_crossentropy
import os,sys

def custom_accuracy_function(mask):
    ### mask: ekta binary mask e.g [1,0,1,0,1,1,1]
    ### 0 represents missing data
    # mask = K.cast(mask, 'float32')
    def custom_accuracy(y_true, y_predict):
        # print(mask.shape, y_true.shape, y_predict.shape)
        # mask = K.cast(mask, 'float32')
        y_pred_labels = K.cast(K.argmax(y_predict, axis=2), 'float32')
        y_true_labels = K.cast(K.argmax(y_true, axis=2), 'float32')
        is_same = K.cast(K.equal(
            y_true_labels, y_pred_labels), 'float32')
        num_same = K.cast(K.sum(is_same * K.cast(mask, 'float32'), axis=1), 'float32')
        lengths = K.cast(K.sum(mask, axis=1), 'float32')
        return K.mean(num_same / (lengths + K.epsilon()), axis=0)
      
    return custom_accuracy

def custom_loss_function(mask):
    def custom_loss(y_true, y_predict):
        y_pred_labels = K.cast(K.argmax(y_predict, axis=2), 'float32')
        y_true_labels = K.cast(K.argmax(y_true, axis=2), 'float32')
        is_same = K.cast(K.equal(y_true_labels, y_pred_labels), 'float32')
        num_same = K.cast(K.sum(is_same * mask, axis=1), 'float32')
        lengths = K.cast(K.sum(mask, axis=1), 'float32')
        return K.cast(1-K.mean(num_same / (lengths + K.epsilon()), axis=0), 'float32')
      
    return custom_loss

def custom_loss_function_2(mask):
    mask_reshaped = mask.reshape(mask.shape[0], mask.shape[1], 1)
    def custom_loss(y_true, y_predict):
        y_true_masked = y_true*mask_reshaped
        y_pred_masked = y_predict*mask_reshaped
        return binary_crossentropy(y_true_masked, y_pred_masked)
      
    return custom_loss

from keras.layers import Embedding, Add, concatenate, Input, Softmax
from keras import backend as K
#keras.activations.softmax(x, axis=-1)
from keras.activations import softmax



def get_model(input_size):

    Input_layer = Input(batch_shape=(None,input_size), name='main_input')
    pos_enc_for_all_trees = Input(batch_shape=(None,input_size), name='pos_enc_for_all_trees')
    
    encoder_layer_embedding = Dense(input_size, activation='relu', use_bias=True) (Input_layer)
    modified_embedding_with_pos_enc = Add()([encoder_layer_embedding, pos_enc_for_all_trees])

    encoder_layer_1 = Dense(int(input_size//1.5), activation='relu', use_bias=True) (modified_embedding_with_pos_enc)
    encoder_layer_2 = Dense(int(input_size//2), activation='relu', use_bias=True) (encoder_layer_1)
    encoder_layer_3 = Dense(int(input_size//2.5), activation='relu', use_bias=True) (encoder_layer_2)

    encoder_layer_4 = Dense(int(input_size//3), activation='relu', use_bias=True) (encoder_layer_3)
    encoder_layer_5 = Dense(int(input_size//4), activation='relu', use_bias=True) (encoder_layer_4)
    decoder_layer_0 = Dense(int(input_size//3), activation='relu', use_bias=True) (encoder_layer_5)

    decoder_layer_1 = Dense(int(input_size//2.5),activation='relu',use_bias=True) (decoder_layer_0)
    decoder_layer_2 = Dense(int(input_size//2),activation='relu',use_bias=True) (decoder_layer_1)
    decoder_layer_3 = Dense(int(input_size//1.5),activation='relu',use_bias=True) (decoder_layer_2)
    decoder_layer_4 = Dense(input_size,activation='relu',use_bias=True) (decoder_layer_3)

    decoder_output = decoder_layer_4

    reshaped = Lambda( lambda x: K.reshape(x, (-1, int(decoder_output.shape[1]//3), 3)))(decoder_output)

    #print(f'Reshaped Shape = {reshaped.shape}')

    final_decoded_layer_output = Softmax(axis=-1)(reshaped)

    autoencoder = Model([Input_layer, pos_enc_for_all_trees], final_decoded_layer_output)
    encoder  = Model([Input_layer, pos_enc_for_all_trees], encoder_layer_4)
    #decoder = Model(encoder_layer_4,final_decoded_layer_output)

    return autoencoder,encoder

def modified_numpy_formation(base_directory):

    Root_Folder = base_directory+"/GT_Numpy"
    # Root_Folder = "drive/MyDrive/25Jan2021/03-10-2021/100g_2_3_runs/"
    # print(os.listdir(Root_Folder+"/Missing_Taxa_GT_Numpy_2-3_taxa"))
   
    Input_Folder = Root_Folder+ "/Whole_GT_Numpy"
    Imputed_Folder = Root_Folder+ "/Imputed_GT_Numpy"
    if not os.path.exists(Imputed_Folder):
        os.mkdir(Imputed_Folder)
    print(os.listdir(Input_Folder))

    Missing_Folder = Root_Folder+ "/Whole_GT_Numpy_modified"

    if not os.path.exists(Missing_Folder):
        os.mkdir(Missing_Folder)
    
    for file_ in os.listdir(Input_Folder):
        ext_ = file_.split(".")

        if(ext_[-1] != "npy"):
            continue
        cnt = file_.split("_whole_arr")[0]

        print(cnt)
        gt_total_taxa_removed = np.load(Input_Folder+"/"+file_)
        print(cnt, gt_total_taxa_removed.shape)
        arr = np.array([0.0,0.0,0.0])
        replace_arr = np.array([1.0/3,1.0/3,1.0/3])
        count = 0
        for idx,x in enumerate(gt_total_taxa_removed):
            for idx_2,y in enumerate(x):
                if(gt_total_taxa_removed[idx][idx_2].any() == arr.any()):
                    bef_ = y.copy()
                    gt_total_taxa_removed[idx][idx_2] = replace_arr
        fl_ = Missing_Folder + "/" + cnt+"_arr.npy"
        np.save(fl_,gt_total_taxa_removed)

def impute(base_directory,num_taxa):

    Root_Folder = base_directory + "/GT_Numpy"
    Input_Folder = Root_Folder+ "/Whole_GT_Numpy"
    Imputed_Folder = Root_Folder+ "/Imputed_GT_Numpy"
    if not os.path.exists(Imputed_Folder):
      os.mkdir(Imputed_Folder)
    print(os.listdir(Input_Folder))

    Missing_Folder = Root_Folder+ "/Whole_GT_Numpy_modified"

    Missing_Alter_Folder = Missing_Folder
    
    print("Doing Folder->",Input_Folder)
    for file_ in os.listdir(Input_Folder):
        ext_ = file_.split(".")
        # print(file_)
        if(ext_[-1] != "npy"):
            continue
        cnt = file_.split("_whole_arr")[0]
        print(cnt,type(cnt))

         

    #         if(int(cnt) >= 10 and int(cnt) <= 20 or int(cnt)<=2):
    #           continue
        print("doing->",cnt)

        gt_total_taxa_removed = np.load(Input_Folder + "/" +cnt+"_whole_arr.npy")
        print(cnt, gt_total_taxa_removed.shape)

        count = 0
        missing_arr_backup = np.load(Missing_Alter_Folder +"/" + cnt + "_arr.npy")

        Train_data_X_arr = gt_total_taxa_removed
        gene_tree_num = Train_data_X_arr.shape[0]
        quartet = 3


        Train_data_X_reshaped = np.transpose(Train_data_X_arr, (1, 0, 2))
        Train_data_X_reshaped = Train_data_X_reshaped.reshape(Train_data_X_reshaped.shape[0],Train_data_X_reshaped.shape[1]*Train_data_X_reshaped.shape[2])

        no_of_gene_trees=int(Train_data_X_reshaped.shape[1]/3)
        three_taxa_seq=Train_data_X_reshaped.shape[0]
        mask=[]
        for i in range (0,three_taxa_seq):
            arr=Train_data_X_reshaped[i]
            mask_row=[]
            for j in range (0,no_of_gene_trees):
                start=j*3
                sum=0

                for k in range(start,start+3):
                    # sum+=arr[k]
                    if(arr[k] == 1.0/3):
                      sum+=0.0
                    else:
                      sum += arr[k]

                mask_row.append(sum)    

            mask.append(mask_row)
        mask=np.array(mask)
        np_mask = mask

        print('np_mask.shape: ', np_mask.shape)
        unique,elem_count = np.unique(np_mask,return_counts=True)
        print(unique,elem_count)


        print('no_of_gene_trees:',no_of_gene_trees, ', quartet:',quartet, ', no_of_gene_trees*quartet:',no_of_gene_trees*quartet)
        # pos_enc(gene_tree_num)
        #=== constants
        NUM_TREES = no_of_gene_trees
        NUM_TAXA = num_taxa
        NUM_ORIENTATION = 3

        #=== positional encoding from Transformer: source: https://github.com/Separius/BERT-keras/blob/master/transformer/embedding.py
        def _get_pos_encoding_matrix(protein_len: int, d_emb: int) -> np.array:
            pos_enc = np.array(
                [[pos / np.power(10000, 2 * (j // 2) / d_emb) for j in range(d_emb)] if pos != 0 else np.zeros(d_emb) for pos in
                range(protein_len)], dtype=np.float32)
            pos_enc[1:, 0::2] = np.sin(pos_enc[1:, 0::2])  # dim 2i
            pos_enc[1:, 1::2] = np.cos(pos_enc[1:, 1::2])  # dim 2i+1
            return pos_enc

        nC4 = lambda x : int(x*(x-1)*(x-2)*(x-3)/(4*3*2))
        print('nC4(NUM_TAXA):', nC4(NUM_TAXA))
        #=== generate pos_enc for any single tree. 
        #=== excepted dataset tensor shape == (NUM_TREES, nC4(NUM_TAXA), NUM_ORIENTATION)  or kXnC3X3
        pos_enc = _get_pos_encoding_matrix(protein_len=nC4(NUM_TAXA), d_emb=NUM_ORIENTATION).reshape(-1, nC4(NUM_TAXA), NUM_ORIENTATION)
        #=== generate pos_enc for all trees.
        pos_enc_for_all_trees = np.repeat(pos_enc, NUM_TREES, axis=0)
        print('pos_enc_for_all_trees.shape: K x nC4 x 3:', pos_enc_for_all_trees.shape)
        pos_enc_for_all_trees = np.transpose(pos_enc_for_all_trees, (1, 0, 2))
        pos_enc_for_all_trees_original = pos_enc_for_all_trees
        print('pos_enc_for_all_trees.shape: nC4 x K x 3:', pos_enc_for_all_trees.shape)
        # global pos_enc_for_all_trees
        pos_enc_for_all_trees = pos_enc_for_all_trees.reshape(pos_enc_for_all_trees.shape[0], pos_enc_for_all_trees.shape[1]*pos_enc_for_all_trees.shape[2])
        print('pos_enc_for_all_trees.shape: nC4 x K * 3:', pos_enc_for_all_trees.shape)


        # dummy_dataset = np.zeros([NUM_TREES, nC4(NUM_TAXA), NUM_ORIENTATION])
        # print('dummy_dataset.shape:', dummy_dataset.shape)
        def step_decay(epoch):
            initial_lrate = 0.0005
            drop = 0.7
            epochs_drop = 10.0
            lrate = initial_lrate * math.pow(drop, math.floor((1+epoch)/epochs_drop))
            lrate = max(0.0001, lrate)
            return lrate

        autoencoder, encoder = get_model(input_size=no_of_gene_trees*quartet)

        # if(no_of_gene_trees < 200):
        #   continue
        autoencoder.summary()

        input_size = int(Train_data_X_arr.shape[1])

   
        PROBAB_OF_NOISE_INCLUSION_FOR_MASKING = .1 # set it to 0.0 if masked learning is not expected

        Train_data_X_reshaped = np.transpose(Train_data_X_arr, (1, 0, 2))
        for __iter__ in range(Train_data_X_reshaped.shape[0]):
            for __iter_2__ in range(Train_data_X_reshaped.shape[1]):
                if Train_data_X_reshaped[__iter__, __iter_2__, 0] != 1./3:
                    biased_coin = np.random.choice(a=[0, 1], 
                                                   p=[PROBAB_OF_NOISE_INCLUSION_FOR_MASKING,
                                                      1. - PROBAB_OF_NOISE_INCLUSION_FOR_MASKING])
                    if biased_coin == 0:
                        Train_data_X_reshaped[__iter__, __iter_2__, :] = np.array([1./3, 1./3, 1./3])


        Train_data_X_reshaped = Train_data_X_reshaped.reshape(Train_data_X_reshaped.shape[0],Train_data_X_reshaped.shape[1]*Train_data_X_reshaped.shape[2])


        Train_data_X_reshaped_3d = np.transpose(Train_data_X_arr, (1, 0, 2))
        adam = Adam(lr=0.001)

        lr_decay = callbacks.LearningRateScheduler(step_decay)
        best_model_file = Root_Folder+'/model_temp_path'
        early_stop = callbacks.EarlyStopping(monitor='loss', patience=500)
        # checkpoint = callbacks.ModelCheckpoint(best_model_file, monitor='custom_accuracy', verbose=1, save_best_only=True, mode='max')
        checkpoint = callbacks.ModelCheckpoint(
            filepath=best_model_file,
            save_weights_only=True,
            monitor='custom_accuracy',
            mode='max',
            save_best_only=True)

        autoencoder.compile(optimizer=adam, 
                           loss = [custom_loss_function_2(mask=np_mask)],
                           sample_weight_mode='temporal',
                           metrics=[custom_accuracy_function(mask=np_mask)])

        autoencoder.fit(x=[Train_data_X_reshaped, pos_enc_for_all_trees],
                       y=Train_data_X_reshaped_3d,
                       epochs=2000, # early_stop is set. so we can set a very high #epochs.
                       batch_size=input_size,
                       sample_weight=np_mask,
                       callbacks=[checkpoint, lr_decay, early_stop],  
                       verbose=1)

        y_hat = autoencoder.predict([Train_data_X_reshaped, pos_enc_for_all_trees])

        imputed_mask_position = 1 - np_mask
        y_hat_reshaped = np.transpose(y_hat, (1, 0, 2))
  
        imputed_mask_position = imputed_mask_position.T
        imputed_mask_position_reshaped = imputed_mask_position.reshape(imputed_mask_position.shape[0], imputed_mask_position.shape[1], 1)
        y_hat_masked = y_hat_reshaped*imputed_mask_position_reshaped
        for i in range(y_hat_reshaped.shape[1]):
            if imputed_mask_position_reshaped[0][i] == 0:
                pass
  
        imputed_array = y_hat_masked + missing_arr_backup
        count_ = 0
        total_ = 0
        s_c = 0
        imputed_array_reserve = imputed_array
        imputed_array_temp = imputed_array

        for i in range(imputed_array.shape[0]):
            for j in range(imputed_array.shape[1]):
                temp = np.argmax(imputed_array[i][j])
                imputed_array[i][j][0] = 0
                imputed_array[i][j][1] = 0
                imputed_array[i][j][2] = 0
                imputed_array[i][j][temp] = 1
        np.save(Imputed_Folder+"/"+cnt+"_imputed_numpy.npy", imputed_array)


