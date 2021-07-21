import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tkt",
    version="1.3.5",
    author="Suprime",
    license = 'MIT',
    author_email="suprime.sendings@gmail.com",
    description="Useful collection of python packages and scripts.",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MOBSkuchen/Toolkit-python",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'httpx',
        'speech_recognition',
        'youtube-search-python',
        'TikTokApi',
        'cryptography',
        'pytube',
        'smtplib',
        'json',
        'random',
        'gtts'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)