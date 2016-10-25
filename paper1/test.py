import pandas as pd

def load_data():
    dataset = pd.read_table("GPL8490-65.txt",index_col = 'ID')
    print(dataset.shape)  #(27578, 38)

    used_dataset = dataset.loc[:,['SourceVersion','Chr','CPG_ISLAND_LOCATIONS']]
    print(used_dataset.head())
    print(used_dataset.shape)
    used_dataset.to_csv("used_dataset.gtf")


if __name__ == '__main__':
    load_data()


"""
           ID        Name IlmnStrand  AddressA_ID  \
0  cg00000292  cg00000292        TOP       990370   
1  cg00002426  cg00002426        TOP      6580397   
2  cg00003994  cg00003994        TOP      7150184   
3  cg00005847  cg00005847        BOT      4850717   
4  cg00006414  cg00006414        BOT      6980731   

                                    AlleleA_ProbeSeq  AddressB_ID  \
0  AAACATTAATTACCAACCACTCTTCCAAAAAACACTTACCATTAAA...      6660678   
1  AATATAATAACATTACCTTACCCATCTTATAATCAAACCAAACAAA...      6100343   
2  AATAATAATAATACCCCCTATAATACTAACTAACAAACATACCCTC...      7150392   
3  TACTATAATACACCCTATATTTAAAACACTAAACTTACCCCATTAA...      1260113   
4  CTCAAAAACCAAACAAAACAAAACCCCAATACTAATCATTAATAAA...      4280093   

                                    AlleleB_ProbeSeq  GenomeBuild Chr  \
0  AAACATTAATTACCAACCGCTCTTCCAAAAAACACTTACCATTAAA...           36  16   
1  AATATAATAACATTACCTTACCCGTCTTATAATCAAACCAAACGAA...           36   3   
2  AATAATAATAATACCCCCTATAATACTAACTAACAAACATACCCTC...           36   7   
3  TACTATAATACACCCTATATTTAAAACACTAAACTTACCCCATTAA...           36   2   
4  CTCGAAAACCGAACAAAACAAAACCCCAATACTAATCGTTAATAAA...           36   7   

     MapInfo  ...   Distance_to_TSS CPG_ISLAND   CPG_ISLAND_LOCATIONS  \
0   28797601  ...             291.0       True   16:28797486-28797825   
1   57718583  ...             369.0       True    3:57716811-57718675   
2   15692387  ...             432.0       True    7:15691512-15693551   
3  176737319  ...             268.0      False                    NaN   
4  148453770  ...             671.0       True  7:148453584-148455804   

   MIR_CPG_ISLAND      RANGE_GB  RANGE_START    RANGE_END RANGE_STRAND  \
0             NaN   NC_000016.8   28797486.0   28797825.0            +   
1             NaN  NC_000003.10   57716811.0   57718675.0            +   
2             NaN  NC_000007.12   15691512.0   15693551.0            -   
3             NaN           NaN          NaN          NaN          NaN   
4             NaN  NC_000007.12  148453584.0  148455804.0            +   

        GB_ACC    ORF  
0  NM_173201.2    487  
1  NM_007159.2   7871  
2  NM_005924.3   4223  
3  NM_006898.4   3232  
4  NM_020781.2  57541  

"""


"""
   SourceVersion Chr   CPG_ISLAND_LOCATIONS
0           36.1  16   16:28797486-28797825
1           36.1   3    3:57716811-57718675
2           36.1   7    7:15691512-15693551
3           36.1   2                    NaN
4           36.1   7  7:148453584-148455804

"""