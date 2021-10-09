import subprocess


def generate_grammar():
    antlr_call_failed = subprocess.call("java org.antlr.v4.Tool > /dev/null", shell=True)
    if antlr_call_failed:
        raise EnvironmentError(
            "Unable to find ANTLR 4\n"
            "\n"
            "ANTLR 4 must be available in your Java classpath to build python-sql-parser.\n"
            "\n"
            "You can download ANTLR 4 here: \n"
            "https://www.antlr.org/download/antlr-4.7.1-complete.jar\n"
            "\n"
            "Once downloaded, you can set your Java classpath using: \n"
            "export CLASSPATH=<path_of_the_download_folder>/antlr-4.7.1-complete.jar\n"
        )
    generation_failed = subprocess.call(
        "java org.antlr.v4.Tool "
        "$(pwd)/src/sqlparser/grammar/SqlBase.g4 "
        "-o $(pwd)/src/sqlparser/generated/ "
        "-Dlanguage=Python3",
        shell=True
    )
    if generation_failed:
        raise EnvironmentError(
            f"An unexpected error occured while generating grammar file (code {generation_failed})\n"
        )


if __name__ == '__main__':
    generate_grammar()
