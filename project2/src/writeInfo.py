import json

def writeInfo(filename, **kwargs):
    """
    At least pass: 
        D, K, H, C: integers
        sigma: float
        num_iter: integer
        hidden_units: "Vanilla"/"GRU"
        regularization: True/False
        lr_strategy: "fixed"/"linear"/"half"
    """
    required = "D sigma num_iter hidden_units regularization lr_strategy".split()
    for req in required:
        if req not in kwargs.keys():
            print("Please pass %s"%req)
            return
    params = {
        "K": 16,
        "H": 8,
        "C": 16,
    }
    params.update(kwargs)
    with open(filename, "w") as file:
        json.dump(params, file, indent=True)

# Example:
# writeInfo("../bla.json", D=8, K=8, sigma=.1, regularization=True,lr_strategy="boe",hidden_units="GRU", num_iter=10)