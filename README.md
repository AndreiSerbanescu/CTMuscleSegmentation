# CTMuscleSegmentation

### Instructions

1) Place source files in ```files/source```

2) Modify ```files/source/Inference.py``` to make compatible with running only on CPU:

Replace on line 88

```checkpoint = torch.load(model_file_name)```

with

```checkpoint = torch.load(model_file_name) if torch.cuda.is_available() else torch.load(model_file_name, map_location=torch.device('cpu'))```