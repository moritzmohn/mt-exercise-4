import re
import argparse
import matplotlib.pyplot as plt

def parse_args():
    '''parse the command line argument'''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--post_log", type=str)
    parser.add_argument("--pre_log", type=str)
    parser.add_argument("--baseline_log", type=str)
    args = parser.parse_args()
    return args



def put_ppls_in_dict(file):

    ppl_dict = {}
    n = 500
    with open(file, 'r') as f:
        for line in f.readlines():
            match = re.search("ppl:\s*\d*.\d*", line)
            if match:
                ppl_dict[n] = match.group().split()[1]
                n += 500
    return ppl_dict
    
def write_table(ppl_baseline, ppl_pre, ppl_post):
    with open("results/table.txt", 'w') as f:
        f.write("validation ppl\tbaseline\tprenorm\t\tpostnorm\n")
        for n in range(500, 41000, 500):
            f.write(str(n))
            f.write("\t\t")
            f.write(ppl_baseline[n])
            f.write("\t\t")
            f.write(ppl_pre[n])
            f.write("\t\t")
            f.write(ppl_post[n])
            f.write("\n")
            
def create_linechart(ppl_baseline, ppl_pre, ppl_post):
    x_axis = ppl_baseline.keys()
    y_axis_pre = [float(i) for i in ppl_pre.values()]
    y_axis_post = [float(i) for i in ppl_post.values()]
    y_axis_baseline = [float(i) for i in ppl_baseline.values()]
    plt.plot(x_axis, y_axis_baseline, label = "baseline")
    plt.plot(x_axis, y_axis_post, label = "postnorm")
    plt.plot(x_axis, y_axis_pre, label = "prenorm")
    plt.legend()
    return plt
    



def main():
    args = parse_args()
    baseline_log = args.baseline_log
    pre_log = args.pre_log
    post_log = args.post_log
    
    #put all perplexities into separate dictionaries
    ppl_baseline = put_ppls_in_dict(baseline_log)
    ppl_pre = put_ppls_in_dict(pre_log)
    ppl_post = put_ppls_in_dict(post_log)
    
    #write a table with all perplexities
    write_table(ppl_baseline,ppl_pre, ppl_post)
    
    #create a line chart and save it
    plt = create_linechart(ppl_baseline, ppl_pre, ppl_post)
    plt.savefig('results/plot.png')
    plt.clf()

if __name__ == '__main__':
    main()