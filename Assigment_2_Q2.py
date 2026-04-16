import re

class DivisionByZeroError(Exception):
    def __init__(self, tree):
        self.tree = tree

def tokenize(expression: str):
    
    cleaned = expression.strip()
    if cleaned == "":
        return []

    # Reject invalid characters early
    if re.search(r"[^\d\s+\-*/()]", cleaned):
        raise ValueError("Invalid character")

    tokens = re.findall(r"\d+|[()+\-*/]", cleaned)
    return tokens


def token_to_string(tokens):

    out = []
    for t in tokens:
        if t.isdigit():
            out.append(f"[NUM:{t}]")
        elif t in "+-*/":
            out.append(f"[OP:{t}]")
        elif t == "(":
            out.append("[LPAREN:(]")
        elif t == ")":
            out.append("[RPAREN:)]")
        else:
            raise ValueError("Unknown token")
    out.append("[END]")
    return " ".join(out)


def format_result(value):
    """
    Whole numbers shown without decimal point.
    Otherwise rounded to 4 decimal places.
    """
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    return str(round(value, 4))


def parse_expression(tokens, index):
    """
    expression := term ((+|-) term)*
    """
    node, value, index = parse_term(tokens, index)

    while index < len(tokens) and tokens[index] in ("+", "-"):
        op = tokens[index]
        index += 1
        right_node, right_value, index = parse_term(tokens, index)

        node = f"({op} {node} {right_node})"
        if op == "+":
            value = value + right_value
        else:
            value = value - right_value

    return node, value, index

#term breakdown
def parse_term(tokens, index):
   
    node, value, index = parse_unary(tokens, index)

    while index < len(tokens):
     
        if tokens[index] in ("*", "/"):
            op = tokens[index]
            index += 1
            right_node, right_value, index = parse_unary(tokens, index)

            node = f"({op} {node} {right_node})"
            if op == "*":
                value = value * right_value
            else:
                if right_value == 0:
                    raise DivisionByZeroError(node)
                value = value / right_value

        # Implicit multiplication
        elif tokens[index] == "(" or tokens[index].isdigit():
            right_node, right_value, index = parse_unary(tokens, index)
            node = f"(* {node} {right_node})"
            value = value * right_value

        else:
            break

    return node, value, index

#Unary Rules : + is not accepted. and Value error messages

def parse_unary(tokens, index):
    
    if index >= len(tokens):
        raise ValueError("Unexpected end of input")

    if tokens[index] == "-":
        index += 1
        node, value, index = parse_unary(tokens, index)
        return f"(neg {node})", -value, index

    if tokens[index] == "+":
        raise ValueError("Unary + not supported")

    return parse_factor(tokens, index)

#Factoring rules : NUM|(expression)
def parse_factor(tokens, index):

    if index >= len(tokens):
        raise ValueError("Unexpected end of input")

    token = tokens[index]

    if token.isdigit():
        return token, float(token), index + 1

    if token == "(":
        index += 1
        node, value, index = parse_expression(tokens, index)

        if index >= len(tokens) or tokens[index] != ")":
            raise ValueError("Missing closing parenthesis")

        index += 1
        return node, value, index

    raise ValueError(f"Unexpected token: {token}")

#Read File function.
def evaluate_expression(expression: str):

    original = expression.rstrip("\n")
    stripped = original.strip()

    if stripped == "":
        return None

    try:
        tokens = tokenize(original)
        token_string = token_to_string(tokens)

        tree, value, index = parse_expression(tokens, 0)

        if index != len(tokens):
            raise ValueError("Extra tokens remain")

        final_value = int(value) if float(value).is_integer() else round(value, 4)

        return {
            "input": original,
            "tree": tree,
            "tokens": token_string,
            "result": final_value
        }

    except DivisionByZeroError as e:
        return {
            "input": original,
            "tree": e.tree,
            "tokens": token_string,
            "result": "ERROR"
        }

    except Exception:
        return {
            "input": original,
            "tree": "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }

#Reads and Writes output 
def evaluate_file(input_path: str) -> list[dict]:
    results = []

    with open(input_path, "r") as infile:
        lines = infile.readlines()

    for line in lines:
        record = evaluate_expression(line)
        if record is not None:
            results.append(record)

# Write output.txt in same directory as input file
    import os
    output_path = os.path.join(os.path.dirname(input_path), "output.txt")

    with open(output_path, "w") as outfile:
        for i, record in enumerate(results):
            outfile.write(f"Input: {record['input']}\n")
            outfile.write(f"Tree: {record['tree']}\n")
            outfile.write(f"Tokens: {record['tokens']}\n")

            if record["result"] == "ERROR":
                outfile.write("Result: ERROR\n")
            else:
                outfile.write(f"Result: {format_result(record['result'])}\n")

            if i != len(results) - 1:
                outfile.write("\n")

    return results

def main():
    import os

    # Get folder where this script lives
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Input file in same folder
    input_path = os.path.join(script_dir, "sample_input.txt")

    print("Running evaluator...")
    print("Input file:", input_path)

    evaluate_file(input_path)

    print("Done. Output written to output.txt")
    
if __name__ == "__main__":
    main()
