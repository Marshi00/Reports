import os
import subprocess
import sys
import time


# launch an application with timeout
# takes the timeout in seconds, the log filename and the launch command as parameters
def launch_app_with_timeout(p_timeout, p_log_name, p_launch_cmd):
    # Runs p_launch_cmd command in a child command-shell
    process = subprocess.Popen(p_launch_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Set the timeout counter to zero
    int_count = 0

    # Loop for p_timeout seconds or until process status = 0 (success)
    while int_count / 100 < p_timeout:
        # Exit the loop if the status is not zero
        if process.poll() is not None:
            sys.stdout.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {p_log_name}, Success, {round(int_count/100, 2)} sec\n")
            sys.stdout.flush()
            break

        int_count += 1
        time.sleep(0.01)

    # Terminate the process if it is still running (status = 0)
    if process.poll() is None:
        process.terminate()
        sys.stdout.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {p_log_name}, Timed Out, {round(int_count/100, 2)} sec\n")
        sys.stdout.flush()


def launch_scadalog(p_timeout, p_file_name):
    # if the scadalog program doesn't exist, pop a message and abort
    scadalog = "c:\\progra~1\\scadalog\\SCADALog.exe"
    if not os.path.exists(scadalog):
        sys.stderr.write(f"{scadalog} can't be found --- aborting\n")
        sys.stderr.flush()
        sys.exit(1)

    # get the current directory
    project_folder = os.path.abspath('.') + "\\"

    # delete the error log file if it exists
    log_file_name = "CollectData.log"
    if os.path.exists(log_file_name):
        os.remove(log_file_name)

    # create the error log file
    with open(log_file_name, 'w') as log_file:
        # read the data
        launch_cmd = f"{scadalog} {project_folder}{p_file_name}.slc /s={project_folder}ReadAll.aut /NoWindow"
        launch_app_with_timeout(p_timeout, f"{p_file_name}.slc", launch_cmd)

        # close the error log file


def main():
    # get the filename from the command-line argument
    file_name = sys.argv[1]

    # call the ScadaLog function to read the data
    launch_scadalog(300, file_name)


if __name__ == '__main__':
    main()
