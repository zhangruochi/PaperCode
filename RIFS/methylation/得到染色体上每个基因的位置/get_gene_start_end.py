"""
处理染色体数据
得到染色体上每个基因的编号和起始结束位置
"""

import csv

def remove_n(data):
    return data.strip("\n")

def get_mRNA():
    with open("hs_ref_GRCh38.p7_chr1.gbs") as f:
        with open("output.txt","a") as result_file:
            while True:
                data = f.readline().strip(" ")
                if data:
                    if len(data) == 0:
                        pass
                    elif data.startswith("mRNA"):
                        every_mRNA_data = []
                        every_mRNA_data.append(data)
                        next_line = f.readline().strip(" ")
                        while next_line[0].isdigit() or next_line[0] == "<":
                            every_mRNA_data.append(next_line)
                            next_line = f.readline().strip(" ")    
                        while True:
                            data = f.readline().strip(" ")
                            if data.startswith('/db_xref="GeneID'): 
                                every_mRNA_data.append(" "+data)   
                                result_file.write("".join(list(map(remove_n,every_mRNA_data))) +"\n")  
                                break
                else:
                    break

def get_id(string):
    return string[string.find("GeneID"):].split(":")[-1].strip('"')

def get_loc(string):
    string_list = string.split("..")
    start = int(string_list[0].split("(")[-1].strip(">").strip("<"))  #not find  return -1
    end = int(string_list[-1].strip(")").strip("<").strip(">"))
    return start,end


def get_id_loc():
    all_dataset = []
    with open("output.txt","r") as f:
        for line in f.readlines():
            data = [item.strip() for item in line.split(" ") if len(item) != 0]
            all_dataset.append(data)

    gene_id = get_id(all_dataset[0][-1])
    start,end = get_loc(all_dataset[0][1])
    start_list=[start]
    end_list = [end]
    
    """
    print(all_dataset[0])
    print(gene_id)
    print(start,end)
    """

    output = open("ultimate_output.csv","w")
    writer = csv.writer(output)
    writer.writerow(["GeneID","startLoc","endLoc"])

    for mRNA in all_dataset[1:]:
        temp_gene_id = get_id(mRNA[-1])
        if temp_gene_id != gene_id:
            writer.writerow([gene_id,min(start_list),max(end_list)])
            gene_id = temp_gene_id
            start_list = []
            end_list = []
            start_list.append(get_loc(mRNA[1])[0])
            end_list.append(get_loc(mRNA[1])[1])
        else:
            start_list.append(get_loc(mRNA[1])[0])
            end_list.append(get_loc(mRNA[1])[1])
      
    output.close()    
                


if __name__ == '__main__':
    get_id_loc()
