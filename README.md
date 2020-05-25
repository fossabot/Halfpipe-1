# Welcome to the mindandbrain/pipeline!

`mindandbrain/pipeline` is a user-friendly software that facilitates reproducible
analysis of fMRI data, including preprocessing, single-subject, and
group analysis. 
It provides state-of-the-art preprocessing using
[`fmriprep`](https://fmriprep.readthedocs.io/), but removes the necessity to
convert data to the
[`BIDS`](https://bids-specification.readthedocs.io/en/stable/) format. 
Common resting-state and task-based fMRI features can the be calculated
on the fly using [`FSL`](http://fsl.fmrib.ox.ac.uk/) with
[`nipype`](https://nipype.readthedocs.io/) for statistics.

> **NOTE:** The `mindandbrain/pipeline` is pre-release software and not yet
> considered production-ready.

<div class="table-of-contents-pre-header"></div>

## Table of Contents

<div class="table-of-contents">
  <ol>
    <li>
      <a href="#getting-started">Getting started</a>
      <ol>
        <li><a href="#container-platform">Container platform</a></li>
        <li><a href="#download">Download</a></li>
      </ol>
    </li>
    <li><a href="#usage-of-the-user-interface">Usage of the user interface</a></li>
    <li><a href="#usage-on-a-high-performance-computing-cluster">Usage on a high-performance computing cluster</a></li>
    <li><a href="#command-line-options">Command line options</a></li>
    <li><a href="#troubleshooting">Troubleshooting</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</div>

## Getting started

The pipeline is distributed as a container, meaning that all software needed for
analysis comes bundled in it. This allows for easier installation on new
systems, and makes data analysis more reproducible, because software versions
are guaranteed to be the same for all users. 

### Container platform

The first step is to install one of the supported container platforms. 
If you're using a high-performance computing cluster, more often than not
`Singularity` will already be available. 

If not, we recommend using the latest version of `Singularity`. However, it can
be somewhat cumbersome to install, as it needs to be built from source. 

The [`NeuroDebian`](https://neuro.debian.net/) package
repository provides an older version of `Singularity` for
[some](https://neuro.debian.net/pkgs/singularity-container.html) Linux
distributions.

In contrast to `Singularity`, `Docker` always requires elevated privileges to
run containers. In other words, every `Docker` user automatically has
administrator privileges on the computer they're using. Therefore, it is
inherently a bad choice for multi-user environments, where the goal is to limit
the access of individual users. `Docker` is the only option that is compatible
with `Mac OS X`. 

Container platform  | Version   | Installation
--------------------|-----------|--------------------------------------------------------------------
**Singularity**     | **3.5.3** | **See <https://sylabs.io/guides/3.5/user-guide/quick_start.html>**
Singularity         | 2.6.1     | `sudo apt install singularity-container`
Docker              |           | See <https://docs.docker.com/engine/install/>

### Download

The second step is to download the `mindandbrain/pipeline` to your computer. 
This requires approximately 5 gigabytes of storage.

Container platform  | Command
--------------------|-------------------------------------------------
Singularity         | `singularity pull shub://mindandbrain/pipeline`
Docker              | `docker pull mindandbrain/pipeline`

`Singularity` version `3.x` creates a container image file called 
`pipeline_latest.sif` in the directory where you run the `pull` command.
For `Singularity` version `2.x` the file is named 
`mindandbrain-pipeline-master-latest.simg`.
Whenever you want to use the container, you need pass `Singularity` the path to
this file.
`Docker` will store the container in its storage base directory, so  it does
not matter from which directory you run the `pull` command.

### Running

The third step is to run the downloaded container. 

Container platform  | Command
--------------------|--------------------------------------------------------------------------
Singularity         | `singularity run --no-home --cleanenv --bind /:/ext pipeline_latest.sif`
Docker              | `docker run --interactive --tty --volume /:/ext mindandbrain/pipeline`

You should now see the user interface.

<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 width="566.36px" height="384.81px" viewBox="0 0 566.36 384.81" style="enable-background:new 0 0 566.36 384.81;"
	 xml:space="preserve">
<style type="text/css">
	.st1{fill:#FFFFFF;border-radius:3px;filter:drop-shadow(0px 0px 20px rgba(0, 0, 0, .7));}
	.st2{fill:#4EB5E1;}
	.st3{fill:#6F7A86;}
	.st4{font-family:SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;}
	.st5{font-size:9.331px;}
</style>
<rect x="43.18" y="43.64" rx="5" class="st1" width="476.75" height="297.03"/>
<g>
	<rect x="63.82" y="272.68" class="st2" width="4.67" height="10.11"/>
	<rect x="59.15" y="313.11" width="443.22" height="10.11"/>
	<g>
		<rect x="126.8" y="70.51" width="19.44" height="20.22"/>
		<rect x="358.52" y="70.51" width="19.44" height="20.22"/>
		<polygon points="339.86,151.38 339.86,161.49 300.98,161.49 300.98,90.73 291.65,90.73 291.65,80.62 320.42,80.62 320.42,151.38 
					"/>
		<path d="M59.15,100.83v80.87h19.44v-20.21h28.77v-60.66H59.15z M87.92,151.38h-9.33v-40.44h9.33V151.38z"/>
		<polygon points="165.68,151.38 165.68,161.49 126.8,161.49 126.8,110.94 117.47,110.94 117.47,100.83 146.24,100.83 
			146.24,151.38 		"/>
		<path d="M175.01,100.83v80.87h19.44v-20.21h28.77v-60.66H175.01z M203.78,151.38h-9.33v-40.44h9.33V151.38z"/>
		<path d="M233.33,100.83v60.66h48.21v-10.11h-28.77v-20.22h28.77v-30.33H233.33z M262.1,121.05h-9.33v-10.11h9.33V121.05z"/>
		<polygon points="397.4,151.38 397.4,161.49 358.52,161.49 358.52,110.94 349.19,110.94 349.19,100.83 377.96,100.83 
			377.96,151.38 		"/>
		<polygon points="454.94,100.83 454.94,161.49 435.5,161.49 435.5,110.94 426.17,110.94 426.17,161.49 406.73,161.49 
			406.73,100.83 		"/>
		<path d="M465.05,100.83v60.66h37.32v-10.11h-17.88v-20.22h17.88v-30.33H465.05z M493.82,121.05h-9.33v-10.11h9.33V121.05z"/>
	</g>	<text transform="matrix(1 0 0 1 59.15 210.4713)" class="st4 st5">Welcome to the mindandbrain/pipeline!</text>	<text transform="matrix(1 0 0 1 59.15 220.5797)" class="st4 st5">You are using version 1.0.0rc2</text>	<text transform="matrix(1 0 0 1 59.15 240.7975)" class="st4 st5">Please report any problems or leave suggestions at</text>	<text transform="matrix(1 0 0 1 59.15 250.9054)" class="st4 st5">https://github.com/mindandbrain/pipeline/issues</text>	<text transform="matrix(1 0 0 1 59.15 271.1227)" class="st4 st5">Specify working directory</text>
	<text transform="matrix(1 0 0 1 59.15 281.2316)" class="st4 st5">[</text>
	<text transform="matrix(1 0 0 1 63.98 281.2316)" class="st1 st4 st5">]</text>
	<text transform="matrix(1 0 0 1 59.15 291.3405)" class="st4 st5">data/</text>
	<text transform="matrix(1 0 0 1 59.15 301.4489)" class="st4 st5">scratch/</text>
	<text transform="matrix(1 0 0 1 59.15 321.6661)" class="st1 st4 st5">[</text>
	<polygon class="st1" points="68.13,318.39 65.72,318.39 65.72,319.62 64.16,318.06 65.72,316.5 65.72,317.72 67.45,317.72 
		67.45,314.47 68.13,314.47 	"/>
	<text transform="matrix(1 0 0 1 68.8101 321.6661)" class="st1 st4 st5">] Ok  [</text>
	<polygon class="st1" points="102.85,318.06 104.4,316.5 104.4,317.72 107.14,317.72 107.14,318.39 104.4,318.39 104.4,319.62 	"/>	<polygon class="st1" points="115.32,319.62 115.32,318.39 112.58,318.39 112.58,317.72 115.32,317.72 115.32,316.5 116.88,318.06 	
		"/>
	<g>		
    <text transform="matrix(1 0 0 1 257.1724 321.6661)" class="st1 st4 st5">l</text>
		<text transform="matrix(1 0 0 1 252.3424 321.6661)" class="st1 st4 st5">e</text>
		<text transform="matrix(1 0 0 1 247.5123 321.6661)" class="st1 st4 st5">c</text>
		<text transform="matrix(1 0 0 1 242.6822 321.6661)" class="st1 st4 st5">n</text>
		<text transform="matrix(1 0 0 1 237.8531 321.6661)" class="st1 st4 st5">a</text>
		<text transform="matrix(1 0 0 1 233.023 321.6661)" class="st1 st4 st5">C</text>		
    <text transform="matrix(1 0 0 1 223.3629 321.6661)" class="st1 st4 st5">]</text>
		<text transform="matrix(1 0 0 1 218.5338 321.6661)" class="st1 st4 st5">c</text>
		<text transform="matrix(1 0 0 1 213.7037 321.6661)" class="st1 st4 st5">-</text>
		<text transform="matrix(1 0 0 1 208.8736 321.6661)" class="st1 st4 st5">l</text>
		<text transform="matrix(1 0 0 1 204.0435 321.6661)" class="st1 st4 st5">r</text>
		<text transform="matrix(1 0 0 1 199.2144 321.6661)" class="st1 st4 st5">t</text>
		<text transform="matrix(1 0 0 1 194.3844 321.6661)" class="st1 st4 st5">c</text>
		<text transform="matrix(1 0 0 1 189.5543 321.6661)" class="st1 st4 st5">[</text>		<text transform="matrix(1 0 0 1 175.065 321.6661)" class="st1 st4 st5">r</text>
		<text transform="matrix(1 0 0 1 170.2349 321.6661)" class="st1 st4 st5">o</text>
		<text transform="matrix(1 0 0 1 165.4058 321.6661)" class="st1 st4 st5">s</text>
		<text transform="matrix(1 0 0 1 160.5758 321.6661)" class="st1 st4 st5">r</text>
		<text transform="matrix(1 0 0 1 155.7457 321.6661)" class="st1 st4 st5">u</text>
		<text transform="matrix(1 0 0 1 150.9166 321.6661)" class="st1 st4 st5">c</text>		<text transform="matrix(1 0 0 1 141.2564 321.6661)" class="st1 st4 st5">e</text>
		<text transform="matrix(1 0 0 1 136.4273 321.6661)" class="st1 st4 st5">v</text>
		<text transform="matrix(1 0 0 1 131.5972 321.6661)" class="st1 st4 st5">o</text>
		<text transform="matrix(1 0 0 1 126.7672 321.6661)" class="st1 st4 st5">M</text>		<text transform="matrix(1 0 0 1 117.108 321.6661)" class="st1 st4 st5">]</text>
	</g>
</g>
</svg>

#### Explanation

Containers are by default isolated from the host computer. This adds security,
but also means that the container cannot access the data it needs for analysis.
The `mindandbrain/pipeline` expects all inputs (e.g., image files and
spreadsheets) and outputs (the working directory) to be places in the path 
`/ext` (see also [--fs-root](#--fs-root)). Using the option `--bind /:/ext`, we
instruct `Singularity` to map all of the host file system (`/`) to that path
(`/ext`). 
You can also modify the option to map only part of the host file system, but
keep in mind that any directories that are not mapped will not be visible later.

`Singularity` passes the host shell environment to the container by default.
This means that in some cases, the host computer's configuration can interfere
with the pipeline. To avoid this, we need to pass the option `--cleanenv`.
`Docker` does not pass the host shell environment by default, so we don't need
to pass an option.

## Usage of the user interface

> **TODO**

## Usage on a high-performance computing cluster

> **TODO**

## Command line options

> **TODO**

### --fs-root

> **TODO**

### --verbose and --debug

> **TODO**

## Troubleshooting

> **TODO**

## Contact

For questions or support, please submit an
[issue](https://github.com/mindandbrain/pipeline/issues/new/choose) or contact
us via e-mail.

 Name        | Role            | E-mail address
-------------|-----------------|------------------------
 Lea Waller  | Developer       | lea.waller@charite.de
 Ilya Veer   | Project manager | ilya.veer@charite.de
 Susanne Erk | Project manager | susanne.erk@charite.de

<style type="text/css">
  h1 { counter-reset: h2-counter; }
  h2 { counter-reset: h3-counter; }
  h2::before {
    counter-increment: h2-counter;
    content: counter(h2-counter) ".\0000a0\0000a0";
  }
  h3::before {
    counter-increment: h3-counter;
    content: counter(h2-counter) "."
             counter(h3-counter) ".\0000a0\0000a0";
  }
  
  .table-of-contents-pre-header + h2::before { 
    counter-increment: none;
    content: normal;
  }
  
  .table-of-contents ol {
    counter-reset: section;
    list-style-type: none;
  }
  .table-of-contents li::before {
    counter-increment: section;
    content: counters(section, ".") ". ";
  }
  
  svg {
    width:100%;
  }
</style>

