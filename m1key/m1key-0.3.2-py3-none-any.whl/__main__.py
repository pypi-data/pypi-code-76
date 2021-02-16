import argparse
from m1key import profile
from m1key import segment
from m1key import resume
from m1key import education
from m1key import thug
from m1key import oneml
from m1key import tree
from m1key import skills
from m1key import website
from m1key import allCommands

def main():
    parser = argparse.ArgumentParser(
        description="A python package of my Tech Journey.")

    parser.add_argument("-i", "--introduce",
                        help="Gives introduction", action="store_true")
    parser.add_argument("-t", "--tree", action="store_true",
                        help="Gives the tree of commands and subcommands")
    parser.add_argument("-w", "--website", action="store_true",
                        help="Takes you to my portfolio website")
    parser.add_argument("-c", "--commands", action="store_true",
                        help="List down all possible commands")

    subparsers = parser.add_subparsers(help="Subcommands")
    # Adding a subparser for project
    parser_project = subparsers.add_parser(
        "project", help="Project information")
    parser_project.add_argument(
        "-s", "--image-segment", dest="image",
        help="""Input an image i.e give location of any image saved on your computer 
                (JPEG,JPG,PNG only), it will extract top 2 dominant colors from the given 
                image and will redraw the entire image with those 2 colors""")
    parser_project.add_argument(
        "-t", "--thug-life", action="store_true", help="Thug Life i.e it will add a prop to your face in realtime.")
    parser_project.add_argument(
        "-o", "--oneml", action="store_true",
        help="""This is one of the major project, bascially this website is a platform 
                where one can see how machine learning algorithms actually work, how 
                gradient changes on adding a point in linear regression, how categorisation 
                is done, what should be the proximity of the point to be classified into a group.""")
    parser_project.set_defaults(name="project")

    # Adding a subparser for Resume
    parser_resume = subparsers.add_parser(
        "resume", help="Helps to download Resume in different format")
    parser_resume.add_argument(
        "-d", "--download", help="Helps to download resume in pdf format", action="store_true")
    parser_resume.set_defaults(name="resume")

    # Adding a subparser for Education
    parser_education = subparsers.add_parser(
        "education", help="Information about my education (Matrix(10),Senior_Secondary(12th),Undegrad(B.Tech))")
    parser_education.add_argument(
        "-a", "--all", action="store_true", help="Gives complete info about my education")
    parser_education.add_argument(
        "-m", "--matrix", action="store_true", help="Gives information about my 10th class results")
    parser_education.add_argument(
        "-x", "--senior-secondary", action="store_true", help="Gives information about my 12th class results")
    parser_education.add_argument(
        "-u", "--undergrad", action="store_true", help="Gives information about my Undergraduation")
    parser_education.set_defaults(name="education")

    # Adding a subparser for skills
    parser_skills = subparsers.add_parser(
        "skills", help="List down all my tech skills")
    parser_skills.add_argument(
        "-a", "--all", action="store_true", help="It shows all my skills with their corresponding percentage")
    parser_skills.set_defaults(name="skills")
    args = parser.parse_args()

    if args.introduce:
        profile.main()
    if args.tree:
        tree.Tree()
    if args.website:
        website.main()
    if args.commands:
        allCommands.main()
    if hasattr(args, "name"):
        if args.name == "project":
            if args.image and not args.thug_life and not args.oneml:
                segment.execute(args.image)
            if args.thug_life and not args.image and not args.oneml:
                print("Loading ..... Please wait ... \nIt will take few seconds, have patience...")
                thug.execute()
            if args.oneml and not args.image and not args.thug_life:
                oneml.main()
        if args.name == "resume":
            if args.download:
                resume.download_resume()
        if args.name == "education":
            if args.all:
                education.main()
            if args.matrix:
                education.matrix()
            if args.senior_secondary:
                education.senior_secondary()
            if args.undergrad:
                education.undergraduation()
        if args.name == "skills":
            skills.main()
