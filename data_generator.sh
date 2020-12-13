# The following allows for a Docker deployment of AnyLog's data generator 
#    :positional arguments:
#        dbms       database name
#        sensor     type of sensor to get data from    {machine,percentagecpu,ping,sin,cos,rand}
#    :optional arguments:
#        -h, --help             show this help message and exit
#        -c, --conn             REST host and port                                                    (default: None)
#        -f, --store-format     format to get data                                                    (default: print)        {rest,file,print}
#        -m, --mode             insert type                                                           (default: streaming)    {file,streaming}
#        -i, --iteration        number of iterations. if set to 0 run continuesly                     (default: 1)
#        -r, --repeat           For machine & ping data number of rows to generate per iteration      (default: 10)
#        -s, --sleep            wait between insert                                                   (default: 0)
#        -p, --prep-dir         directory to prepare data in                                          (default: $HOME/AnyLog-Network/data/prep)
#        -w, --watch-dir        directory for data ready to be stored                                 (default: $HOME/AnyLog-Network/data/watch)


# Get help 
if [[ ${help} == true ]] 
then 
    python3 /app/Sample-Data-Generator/data_generator.py --help 
    exit 1 
fi 

# Validate dbms & sensor are set 
error='' 
status=0 
if [[ -z ${dbms} ]] 
then 
    error="dbms cannot be empty" 
    status=1 
fi 
if [[ -z ${sensor} ]] && [[ ${status} -eq 1 ]] 
then
    error="${error} & sensor cannot be empty\nsensor options:\n\tmachine\n\tpercentagecpu\n\tping\n\tcos\n\tsin\n\trand\n" 
    status=2
elif [[ -z ${sensor} ]]
then 
    error="sensor cannot be empty\nsensor options:\n\tmachine\n\tpercentagecpu\n\tping\n\tcos\n\tsin\n\trand\n" 
    status=1 
fi 

if [[ ${status} -gt 0 ]] 
then 
    printf "${error}" 
    exit 1 
fi 


# configure optional arguments, if empty 
if [[ -z ${conn}         ]] ; then conn=None                 ; fi 
if [[ -z ${store_format} ]] ; then store_format='print'      ; fi 
if [[ -z ${mode}         ]] ; then mode=streaming            ; fi 
if [[ -z ${iteration}    ]] ; then iteration=1               ; fi 
if [[ -z ${repeat}       ]] ; then repeat=10                 ; fi 
if [[ -z ${sleep}        ]] ; then sleep=0                   ; fi 
if [[ -z ${prep_dir}     ]] ; then prep_dir=/app/data/prep   ; fi 
if [[ -z ${watch_dir}    ]] ; then watch_dir=/app/data/watch ; fi 


# Run python script 
python3 /app/Sample-Data-Generator/data_generator.py ${dbms} ${sensor} -c ${conn} -f ${store_format} -m ${mode} -i ${iteration} -r ${repeat} -s ${sleep} -p ${prep_dir} -w ${watch_dir}

