from setuptools import setup

setup(name='compiler_oj',
      license='MIT',
      packages=['compiler_oj'],
      url="https://github.com/Engineev/compiler-offline-judge",
      author='Yunwei Ren',
      entry_points={
        'console_scripts': ['compiler-oj=compiler_oj.command_line:main']
      })
