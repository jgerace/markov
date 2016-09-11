import argparse
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chain_len', type=int, default=4,
                        help='length of the Markov chain')
    parser.add_argument('--input_file', type=str, required=True,
                        help='path to file with input text')
    parser.add_argument('--num_chars', type=int, required=True,
                        help='number of chars in output')

    args = parser.parse_args()

    markov_chain(args=args)

def markov_chain(args=None):
    table = create_table(args=args)
    generate_text(args=args, table=table)

def create_table(args=None):
    table = {}
    text = None
    
    with open(args.input_file, 'r') as fin:
        text = fin.read()

    if not text:
        raise Exception('No input text')

    for idx in xrange(len(text)):
        chain = text[idx:idx+args.chain_len]
        after = text[idx+args.chain_len:idx+(2*args.chain_len)]
        if not table.get(chain):
            table[chain] = {}

        if not table[chain].get(after):
            table[chain][after] = 1
        else:
            table[chain][after] = table[chain][after] + 1

    return table

def generate_text(args=None, table=None):
    choice = random.choice(table.keys())
    output = choice

    for idx in xrange(args.num_chars / args.chain_len):
        new_char = get_random_next(table[choice])
        if new_char:
            choice = new_char
            output += new_char
        else:
            choice = random.choice(table.keys())

    print output

def get_random_next(choices=None):
    total = sum(choices[key] for key in choices)
    rand = random.randint(1, total)

    for key in choices:
        weight = choices[key]
        if rand <= weight:
            return key
        rand = rand - weight

if __name__ == '__main__':
    try:
        main();
    except Exception as e:
        print 'Error: %s ' % (e.message,)
        
