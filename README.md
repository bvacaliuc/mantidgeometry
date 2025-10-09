[![Code Climate](https://codeclimate.com/github/mantidproject/mantidgeometry/badges/gpa.svg)](https://codeclimate.com/github/mantidproject/mantidgeometry)


This repository is intended to store the python helper scripts for
generating the Mantid IDFs. Each instrument is supported in its own
python script.

Using
-----
The classes that will help with creating geometry are [helper.py](helper.py), [rectangle.py](rectangle.py), and [sns_column.py](sns_column.py). A quick example

```python
from helper import MantidGeom

inst_name = "VISION"

xml_outfile = inst_name+"_Definition.xml"

comment = " Created by G. Fawkes "
valid_from = "2013-11-5 00:00:01"

instr = MantidGeom(inst_name, comment=comment, valid_from=valid_from)
instr.addSnsDefaults(indirect=True)
instr.addComment("SOURCE AND SAMPLE POSITION")
instr.addModerator(-16.0)
instr.addSamplePosition()

instr.writeGeom(xml_outfile)
```

Testing
-------
The test harness is small and will (generically) generate false positives, but you should run it anyway.

1. Do your work and commit it locally
2. `git checkout origin/master` or just `git checkout master` if you did your work on a branch
3. `./test_unchanged.py --setup` will create all the geometry files before you do your work
4. `git checkout -` to go back to your latest commit/branch
5. `./test_unchaged.py` to see what (if anything) has changed

There are also tests for some of the helper classes. This is run automatically by travis-ci
and can be found in the `.travis.yml` in the `script` section.

[![Stories in Ready](https://badge.waffle.io/mantidproject/mantidgeometry.png?label=ready)](https://waffle.io/mantidproject/mantidgeometry)
[![Travis-CI Build Status](https://travis-ci.org/mantidproject/mantidgeometry.svg)](https://travis-ci.org/mantidproject/mantidgeometry)

Specific
--------

These are specific instructions for the use of the NOWD geometry files.  These are an auxiliary system used to help integrate a new generation detector into the POWGEN (PG3) instrument.

1. you will need a 'mantidgeometry' conda-forge environment

```
mamba env create -f mantidgeometry.yml
```

2. To generate any of the nowd_* geometry files, run the following in the 'mantidgeometry' environment:
```
mamba activate mantidgeometry
(mantidgeometry) python nowd_geometry_154x7.py
```
It should give the following output:
```
writing NOWD_Definition_154x7.xml
```

3. You will need to *manually* edit the resulting `NOWD_Definition_154x7.xml` file:
```
26c26
<     <location />
---
>     <location/>
33,35c33
<   <component type="North">
<     <location />
<   </component>
---
>   <component type="North"/>
37,45c35,37
<     <component type="Column13">
<       <location />
<     </component>
<     <component type="Column19">
<       <location />
<     </component>
<     <component type="Column21">
<       <location />
<     </component>
---
>     <component type="Column13"/>
>     <component type="Column19"/>
>     <component type="Column21"/>
```

You will need the edits in the '<' section.  Example edited files are provided in `NOWD_Definition_154x7.chk` and `NOWD_Definition_462x32.chk`.

4. After you edit the definition file to remove the errors, you can test loading it in mantid.  **NOTE: you need to use a different environment to do that!**
**NOTE: I had problems on my MacOS using a simple `mamba env create -f mantid.yml`, but I was able to use the hint posted in this [issue](https://github.com/mamba-org/mamba/issues/3951) to workaround an issue with not being able to create the environment.

Use:
```
TMPDIR=/tmp mamba env create --file mantid.yml
```

There is an example `mantid.yml` file that can be used for validating the environment.

I apologize if this is complicated, I'm trying not to make *too many* deviations from the path.

#### on your own computer, you might do:
```
mamba activate mantid
(mantid) python python nowd_geometry_test.py
```
It should give the following output:
```
FrameworkManager-[Notice] Welcome to Mantid 6.13.1
FrameworkManager-[Notice] Please cite: http://dx.doi.org/10.1016/j.nima.2014.07.029 and this release: http://dx.doi.org/10.5286/Software/Mantid6.13.1
DownloadInstrument-[Error] Error in execution of algorithm DownloadInstrument:
DownloadInstrument-[Error] Access to file denied
CreateSampleWorkspace-[Notice] CreateSampleWorkspace started
CreateSampleWorkspace-[Notice] CreateSampleWorkspace successful, Duration 0.00 seconds
LoadInstrument-[Notice] LoadInstrument started
InstrumentDefinitionParser-[Notice] Geometry cache is not available
InstrumentDefinitionParser-[Notice] Creating cache in /Users/6ov/.mantid/instrument/geometryCache/NOWD0ab15eb8332551d81f83ba88e53f5d1746d81485.vtp
LoadInstrument-[Notice] LoadInstrument successful, Duration 0.01 seconds
Default workspace has instrument: NOWD with 0 parameters
CreateSampleWorkspace-[Notice] CreateSampleWorkspace started
CreateSampleWorkspace-[Notice] CreateSampleWorkspace successful, Duration 0.00 seconds
LoadInstrument-[Notice] LoadInstrument started
InstrumentDefinitionParser-[Notice] Geometry cache is not available
InstrumentDefinitionParser-[Notice] Creating cache in /Users/6ov/.mantid/instrument/geometryCache/NOWDe35c05d05abce0a3556115bce67fd09d23d87f9f.vtp
LoadInstrument-[Notice] LoadInstrument successful, Duration 0.06 seconds
Default workspace has instrument: NOWD with 0 parameters
```

The reason for the 'Access to file denied' is because you are not on the ORNL instrument file system so certain defaults are inaccessible.  There may be ways to mitigate this in the future...

#### on analysis.sns.gov, you would do:
```
source /opt/anaconda/bin/activate /opt/anaconda/envs/mantid
(mantid) python test_geometry.py
```
It should give the following output:
```
FrameworkManager-[Notice] Welcome to Mantid 6.13.1.2
FrameworkManager-[Notice] Please cite: http://dx.doi.org/10.1016/j.nima.2014.07.029 and this release: http://dx.doi.org/10.5286/Software/Mantid6.13.1
CreateSampleWorkspace-[Notice] CreateSampleWorkspace started
CreateSampleWorkspace-[Notice] CreateSampleWorkspace successful, Duration 0.01 seconds
LoadInstrument-[Notice] LoadInstrument started
LoadInstrument-[Notice] LoadInstrument successful, Duration 0.01 seconds
Default workspace has instrument: NOWD with 0 parameters
CreateSampleWorkspace-[Notice] CreateSampleWorkspace started
CreateSampleWorkspace-[Notice] CreateSampleWorkspace successful, Duration 0.00 seconds
LoadInstrument-[Notice] LoadInstrument started
LoadInstrument-[Notice] LoadInstrument successful, Duration 0.11 seconds
Default workspace has instrument: NOWD with 0 parameters
```
