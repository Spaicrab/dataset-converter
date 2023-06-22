# Description
Converts a dataset's labels from a format to another.
Currently, the available format wrappers are:
- Yolo
- VOC
- Coco (Only one label per image)

# Syntax
```
dataset-converter <INPUT_PATH> <OUTPUT_PATH> <INPUT_WRAPPER> <OUTPUT_WRAPPER> [--filter-classes (-f) <CLASS> [<CLASS> ...]] [--no-img (-n)]
```

# Arguments
``` <INPUT_PATH> ``` Input directory with the images and their labels.

``` <OUTPUT_PATH> ``` Output directory that will contain all converted labels and their images (if there isn't --no-img).

``` <INPUT_WRAPPER> ``` Input Wrapper.

``` <OUTPUT_WRAPPER> ``` Output Wrapper.

``` [--filter-classes (-f) <CLASS> [<CLASS> ...]] ``` List of classes to be filtered. All images that don't contain at least one of these classes will be ignored. - filtering is disabled by default

``` [--no-img (-n)] ``` Don't copy images to <OUTPUT_PATH>.

# Usage
```
converter = DatasetConverter()
converter.convert(
    in_dir, out_dir, in_wrap, out_wrap, [classes], [copy], [recursive]
)
```
where:

**in_dir** and **out_dir** are both directory paths

**in_wrap** and **out_wrap** are both strings

**classes** is a list

**copy** and **recursive** are booleans