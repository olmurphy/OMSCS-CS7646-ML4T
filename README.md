<!-- Improved compatibility of back to top link: See: https://github.com/olmurphy/OMSCS-CS7646-ML4T/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Open Issues](https://img.shields.io/github/issues-raw/olmurphy/OMSCS-CS7646-ML4T?state=open&style=for-the-badge)](https://github.com/olmurphy/OMSCS-CS7646-ML4T/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/olmurphy/OMSCS-CS7646-ML4T?style=for-the-badge)](https://github.com/olmurphy/OMSCS-CS7646-ML4T/issues?q=is%3Aclosed)
[![Commit Activity](https://img.shields.io/github/commit-activity/y/olmurphy/OMSCS-CS7646-ML4T?style=for-the-badge)](https://github.com/olmurphy/OMSCS-CS7646-ML4T/graphs/commit-activity)
[![Repo Size](https://img.shields.io/github/repo-size/olmurphy/OMSCS-CS7646-ML4T?style=for-the-badge)](https://github.com/olmurphy/OMSCS-CS7646-ML4T)
[![Top Language](https://img.shields.io/github/languages/top/olmurphy/OMSCS-CS7646-ML4T?style=for-the-badge)](https://github.com/olmurphy/OMSCS-CS7646-ML4T/search?l=YOUR_TOP_LANGUAGE)
[![Last Commit](https://img.shields.io/github/last-commit/olmurphy/OMSCS-CS7646-ML4T?style=for-the-badge)](https://github.com/olmurphy/OMSCS-CS7646-ML4T/main)
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/owenmurphy2022/)
![Created At](https://img.shields.io/github/created-at/olmurphy/OMSCS-CS7646-ML4T?style=for-the-badge
)

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/olmurphy/OMSCS-CS7646-ML4T">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Machine Learning for Trading</h3>

  <p align="center">
    Project repo
    <br />
    <a href="https://github.com/olmurphy/OMSCS-CS7646-ML4T"><strong>Explore the docs »</strong></a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is for the Machine Learning for Trading (OMSCS CS7646) course, where the goal is to build a complete, simulated trading system piece by piece.  Each project builds on the last, culminating in a capstone project that synthesizes all the learned concepts into a practical, operational AI trading agent. The final system will demonstrate the application of machine learning principles to real-world financial markets.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This project uses several key Python libraries for its functionality.
- SciPy: A library used for scientific and technical computing.
- Python: The programming language for all code.
- Matplotlib: A plotting library used for data visualization.
- Pandas: A powerful data manipulation and analysis library.
- NumPy: A fundamental package for scientific computing with Python.

[![Python][Python.org]][Python-url]
[![NumPy][Numpy.org]][Numpy-url] 
[![Pandas][Pandas.pydata.org]][Pandas-url] 
[![Matplotlib][Matplotlib.org]][Matplotlib-url] 
[![SciPy][Scipy.org]][Scipy-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy of this project up and running, follow these steps.

### Prerequisites

This project requires Miniconda to manage the environment and dependencies.

### Installation

1. Activate your Miniconda environment.
    ```bash
    source ~/miniconda3/bin/activate
    ```
2. Create and activate the project's conda environment.
   ```bash
   conda env create --file environment.yml
   conda activate ml4t
   ```
3. Download the necessary data files from the course website:
    - https://gatech.instructure.com/courses/457942/files/64546675/download?download_frd=1
    - https://gatech.instructure.com/courses/457942/files/64546685/download?download_frd=1

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run a specific project file, use the following command. The PYTHONPATH is set to ensure the program can locate all required modules.

```
PYTHONPATH=../:. python <name_of_file>
```

For more information on the course and using the autograder, refer to the official course website.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/olmurphy/OMSCS-CS7646-ML4T/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=olmurphy/OMSCS-CS7646-ML4T" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Course Website: http://lucylabs.gatech.edu/ml4t/

Owen Li Murphy - [@owenmurphy222](https://twitter.com/owenmurphy2022) - omurphy8@gatech.edu

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This project is part of the Machine Learning for Trading (OMSCS CS7646) course at Georgia Tech.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/olmurphy/OMSCS-CS7646-ML4T.svg?style=for-the-badge
[contributors-url]: https://github.com/olmurphy/OMSCS-CS7646-ML4T/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/olmurphy/OMSCS-CS7646-ML4T.svg?style=for-the-badge
[forks-url]: https://github.com/olmurphy/OMSCS-CS7646-ML4T/network/members
[stars-shield]: https://img.shields.io/github/stars/olmurphy/OMSCS-CS7646-ML4T.svg?style=for-the-badge
[stars-url]: https://github.com/olmurphy/OMSCS-CS7646-ML4T/stargazers
[issues-shield]: https://img.shields.io/github/issues/olmurphy/OMSCS-CS7646-ML4T.svg?style=for-the-badge
[issues-url]: https://github.com/olmurphy/OMSCS-CS7646-ML4T/issues
[license-shield]: https://img.shields.io/github/license/olmurphy/OMSCS-CS7646-ML4T.svg?style=for-the-badge
[license-url]: https://github.com/olmurphy/OMSCS-CS7646-ML4T/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/owenmurphy2022
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[Numpy.org]: https://img.shields.io/badge/Numpy-013243?style=for-the-badge&logo=numpy&logoColor=white
[Numpy-url]: https://numpy.org/

[Pandas.pydata.org]: https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/

[Matplotlib.org]: https://img.shields.io/badge/Matplotlib-013243?style=for-the-badge&logo=matplotlib&logoColor=white
[Matplotlib-url]: https://matplotlib.org/

[Scipy.org]: https://img.shields.io/badge/SciPy-82BEE9?style=for-the-badge&logo=scipy&logoColor=white
[Scipy-url]: https://scipy.org/

1. 
`source ~/miniconda3/bin/activate`

2. 
```
conda env create --file environment.yml
conda activate ml4t
```

3. `PYTHONPATH=../:. python <name_of_file>`

## Make sure to have this

Download https://gatech.instructure.com/courses/457942/files/64546675/download?download_frd=1

Download https://gatech.instructure.com/courses/457942/files/64546685/download?download_frd=1


