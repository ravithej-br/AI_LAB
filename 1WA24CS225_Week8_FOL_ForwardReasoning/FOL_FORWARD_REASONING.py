
# WEEK 8: FOL FORWARD REASONING
# Generalized Forward Chaining Algorithm

# 1. Convert predicate string into tuple
def parse_atom(atom):

    atom = atom.strip()

    predicate = atom[:atom.index("(")].strip()

    arguments = atom[atom.index("(") + 1:atom.rindex(")")]

    if not arguments.strip():
        return (predicate, ())

    args = tuple(x.strip() for x in arguments.split(","))

    return (predicate, args)


# 2. Convert tuple into readable predicate
def format_atom(atom):

    predicate, arguments = atom

    return predicate + "(" + ", ".join(arguments) + ")"


# 3. Apply substitutions to variables
def substitute(atom, substitution):

    predicate, arguments = atom

    new_args = []

    for arg in arguments:

        while arg.startswith("?") and arg in substitution:
            arg = substitution[arg]

        new_args.append(arg)

    return (predicate, tuple(new_args))


# 4. Match a rule premise with a known fact
def match(pattern, fact, substitution):

    if pattern[0] != fact[0]:
        return None

    if len(pattern[1]) != len(fact[1]):
        return None

    result = substitution.copy()

    for p, f in zip(pattern[1], fact[1]):

        if p.startswith("?"):

            if p in result:

                if result[p] != f:
                    return None

            else:
                result[p] = f

        elif p != f:
            return None

    return result


# 5. Find substitutions satisfying all premises
def find_substitutions(premises, facts):

    results = []

    def backtrack(index, substitution):

        if index == len(premises):
            results.append(substitution.copy())
            return

        premise = substitute(
            premises[index], substitution
        )

        for fact in facts:

            new_substitution = match(
                premise, fact, substitution
            )

            if new_substitution is not None:

                backtrack(
                    index + 1,
                    new_substitution
                )

    backtrack(0, {})

    return results


# 6. Forward Chaining Algorithm
def forward_chaining(facts, rules, query):

    kb = list(facts)
    known = set(kb)

    iteration = 1

    print("\n========== FORWARD CHAINING ==========")

    print("\nInitial Knowledge Base:")

    for fact in kb:
        print(format_atom(fact))

    # Repeat until no new facts are derived
    while True:

        print("\nIteration", iteration)

        new_facts = []

        # Check every rule
        for premises, conclusion in rules:

            substitutions = find_substitutions(
                premises, kb
            )

            for substitution in substitutions:

                derived = substitute(
                    conclusion, substitution
                )

                # Avoid duplicate facts
                if derived not in known and derived not in new_facts:

                    new_facts.append(derived)

                    print("\nRule applied with:", substitution)

                    print("Derived:", format_atom(derived))

        # Stop when no new facts are found
        if not new_facts:

            print("\nNo new facts can be derived.")
            break

        # Add newly derived facts to KB
        for fact in new_facts:

            kb.append(fact)
            known.add(fact)

        iteration += 1

    # Display final Knowledge Base
    print("\n========== FINAL KNOWLEDGE BASE ==========")

    for fact in kb:
        print(format_atom(fact))

    # Check query
    print("\n========== QUERY RESULT ==========")

    print("Query:", format_atom(query))

    if query in known:

        print("Result: TRUE")
        print("Query successfully proved.")

        return True

    else:

        print("Result: FALSE")
        print("Query could not be proved.")

        return False


# 7. MAIN PROGRAM
if __name__ == "__main__":

    # Input initial facts
    facts = []

    n = int(input("Enter number of initial facts: "))

    print("\nEnter facts (Example: Human(Ram)):")

    for i in range(n):

        fact = input("Fact: ")

        facts.append(parse_atom(fact))

    # Input rules
    rules = []

    m = int(input("\nEnter number of rules: "))

    print("\nEnter rules in the format:")
    print("A(?x);B(?x)->C(?x)")
    print("Use semicolon (;) to separate premises.")

    for i in range(m):

        rule = input("Rule: ")

        left, right = rule.split("->")

        # Split premises using semicolon
        premises = [
            parse_atom(x.strip())
            for x in left.split(";")
        ]

        # Parse conclusion
        conclusion = parse_atom(right.strip())

        rules.append((premises, conclusion))

    # Input query
    query = parse_atom(
        input("\nEnter query to prove: ")
    )

    # Execute forward chaining
    forward_chaining(facts, rules, query)
