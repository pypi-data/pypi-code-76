def constraints_to_internal(constraints):
    labels = "".join(set("".join(constraints)))
    numbered_constraints = []
    for constraint in constraints:
        c = ""
        for i in range(len(constraint)):
            c += str(labels.find(constraint[i]))
        numbered_constraints.append(c)
    constraints = numbered_constraints
    configurations = {label: [] for label in range(len(labels))}
    for c in constraints:
        configurations[int(c[1])].append((int(c[0]), int(c[2])))
    return configurations, labels

print(constraints_to_internal(["AAB"]))