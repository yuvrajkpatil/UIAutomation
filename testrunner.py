import os
import time
import shutil
import sys
import robot
import builtins


def _move_logs(test_list_file, latest_logs_dir):
    """
    This method copies Logs from Logs\\latest folder into Logs\\
    :param test_list_file: Tests path which was given in execution command
    :param latest_logs_dir: latest logs directory path
    :return: None
    """
    if '.' in test_list_file:
        folder_name = os.path.basename(test_list_file).split('.')[0]
    else:
        folder_name = test_list_file.rstrip('\\')
    folder_name = "%s-%s" % (folder_name, time.strftime("%d%B%Y.%I%M%S"))
    print("Copied Logs Directory Name: %s" % folder_name)

    # Copy logs from source to destination directory
    destination = os.path.join('Logs', folder_name)
    try:
        shutil.copytree(latest_logs_dir, destination)
    except OSError as exc:
        print("Error copying/archiving logs...")


def __get_tags(tags):
    """
    This method creates a 'OR' separated string of multiple tags from ',' separated string
    :param tags: single tag or ',' separated string of multiple tags. (Mandatory arg)
    :return: single tag or 'OR' separated string if multiple tags
    """
    all_tags = ''
    alltags = tags.split(',')
    for tag in alltags:
        all_tags += tag + 'OR'
    all_tags = all_tags.rstrip('OR')
    return all_tags


def main():
    # Read options from command line
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-t", "--test", dest="testlist", default='Tests\\', help="Specify path of TestList to be executed")
    parser.add_option("-b", "--browser", dest="browser", default='gc', help="Specify which browser to use for execution. E.g. ff, gc")
    parser.add_option("-i", "--includetag", dest="testincludetags", default=False, help="Run tests of given tag only. E.g. sanity, regression")
    parser.add_option("-e", "--excludetag", dest="testexcludetags", default=False, help="Exclude tests of given tag. E.g. sanity, regression")
    parser.add_option("-u", "--baseurl", dest="baseurl", default='https://www.saucedemo.com/', help='Base URL of application')
    options, __ = parser.parse_args()
    print("Options: %s" % options)

    # Check if testlist is provided. If not exit the execution
    if not options.testlist:
        print("Test Suite is Not Specified")
        sys.exit()
    builtins.browser = options.browser.lower()
    builtins.baseurl = options.baseurl
    print("Base URL: %s, Browser: %s" % (baseurl, browser))
    latest_log_folder = 'latest'
    runoptions = {}
    runoptions['outputdir'] = os.path.join('Logs', latest_log_folder)

    if options.testincludetags:
        runoptions['include'] = __get_tags(options.testincludetags)
    if options.testexcludetags:
        runoptions['exclude'] = __get_tags(options.testexcludetags)

    # Cleanup latest log folder
    latest_folder = os.path.join('Logs', latest_log_folder)
    try:
        shutil.rmtree(latest_folder, ignore_errors=True)
        print("Cleanup latest log folder successful...")
    except:
        print("Warning: Cleanup latest log folder failed...")

    # Create the latest log folder if does not exist
    if not os.path.exists(latest_folder):
        time.sleep(1)
        os.makedirs(latest_folder)

    print("Final Run Options: %s" % runoptions)
    robot_return_code = robot.run(options.testlist, variable=['baseurl:%s' % baseurl, 'browser:%s' % browser],
                                  **runoptions)
    robot.rebot(runoptions['outputdir'] + "\\output.xml", **runoptions)
    print("TESTRUN COMPLETED")
    print("Trying to copy/archive logs...")
    _move_logs(options.testlist, runoptions['outputdir'])
    return robot_return_code

if __name__ == "__main__":
    main()
