import argparse
import subprocess
import multiprocessing as mp


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute ISiCLE simulations.')

    config = parser.add_argument_group('Snakemake configuration')
    config.add_argument('--config', required=True, help='Path to ISiCLE configuration file.')

    # cluster mode not yet supported through this interface
    config.add_argument('--cluster-config', help='Path to cluster execution configuration file.')

    config.add_argument('--cores', type=int, default=mp.cpu_count(), help='Number of cores used for execution (ignored for cluster execution).')
    config.add_argument('--dryrun', action='store_true', help='Perform a dry run.')

    prop = parser.add_argument_group('Property calculation')
    mprop = prop.add_mutually_exclusive_group(required=True)
    mprop.add_argument('--ccs', action='store_true', help='Calculate collision cross section.')
    mprop.add_argument('--chem-shifts', action='store_true', help='Calculate NMR chemical shifts.')

    mode = parser.add_argument_group('Calculation mode (CCS only)')
    mmode = mode.add_mutually_exclusive_group(required=True)
    mmode.add_argument('--standard', action='store_true', help='Standard calculation mode.')
    mmode.add_argument('--lite', action='store_true', help='Lite calculation mode.')

    args = parser.parse_args()

    if args.ccs is True:
        if args.standard is True:
            cmd = 'snakemake --snakefile isicle/rules/ccs_standard.snakefile --cores %s --configfile %s -k --rerun-incomplete' % (args.cores, args.config)
        elif args.lite is True:
            cmd = 'snakemake --snakefile isicle/rules/ccs_lite.snakefile --cores %s --configfile %s -k --rerun-incomplete' % (args.cores, args.config)
    elif args.chem_shifts is True:
        cmd = 'snakemake --snakefile isicle/rules/chemshifts.snakefile --cores %s --configfile %s -k --rerun-incomplete' % (args.cores, args.config)

    if args.dryrun:
        cmd += ' --dryrun'

    subprocess.call(cmd, shell=True)
