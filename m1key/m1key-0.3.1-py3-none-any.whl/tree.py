from anytree import Node, RenderTree

"""m1key \n
                |-h \n
                |-i  \n
                |-w  \n
                |project \n
                    |-h \n
                    |-s \n
                    |-t \n
                    |-o \n
                |resume \n
                    |-h \n
                    |-d \n
                |education \n
                    |-h \n
                    |-m \n
                    |-x \n
                    |-u \n
"""

def Tree():
    m1key = Node("m1key")
    helpM1key = Node("-h", parent=m1key)
    introduce = Node("-i", parent=m1key)
    website = Node("-w", parent=m1key)
    commands = Node("-c", parent=m1key)
    project = Node("project", parent=m1key)
    helpProject = Node("-h", parent=project)
    image = Node("-s image_location_from_your_computer", parent=project)
    thug = Node("-t", parent=project)
    oneml = Node("-o", parent=project)
    resume = Node("resume", parent=m1key)
    helpResponse = Node("-h", parent=resume)
    downloaded = Node("-d", parent=resume)
    education = Node("education", parent=m1key)
    helpEducation = Node("-h", parent=education)
    matrix = Node("-m", parent=education)
    secondary = Node("-s", parent=education)
    undergrad = Node("-u", parent=education)
    skills = Node("skills",parent=m1key)
    helpSkills = Node("-h", parent=skills)
    allSkills = Node("-a", parent=skills)
    
    for pre,fill,node in RenderTree(m1key):
        print(pre,node.name)
