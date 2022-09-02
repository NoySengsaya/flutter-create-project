#!/usr/bin/python3
import os
import sys
import argparse

import shutil


parser = argparse.ArgumentParser(prog="./flutter-create-project.py", description="Flutter create project")
parser.add_argument("-p", dest="dep_filename", help="List of dependencies to add")
parser.add_argument("-d", dest="devdep_filename",  help="List of dev dependencies to add")
parser.add_argument("-o", dest="org", help="Application package id [com.example.app]")
parser.add_argument("-n", dest="appName", help="Application name")
args = parser.parse_args()

packages = []
devPackages = []

org = args.org
name = args.appName
capitalizeName = name.capitalize()

linuxPath = "linux/"
webPath= "web/"
windowsPath = "windows/"
macOSPath = "macos/"

cmd = "flutter create --org " + org + " --project-name " + name + " ."

with open(args.dep_filename) as dependencies:
    packages = [line.rstrip() for line in dependencies]
    

for p in packages:
    print("adding list of packages to commands ... ")
    cmd += " && flutter pub add " + packages[packages.index(p)]

with open(args.devdep_filename) as devDependencies:
    devPackages = [line.rstrip() for line in devDependencies]

for d in devPackages:
    print("adding list of dev packages to commands ... ")
    cmd += " && flutter pub add --dev " + devPackages[devPackages.index(d)]

os.system(cmd)


main = """
import 'package:flutter/material.dart';

void main() => runApp(const {capitalizeName}());

class {capitalizeName} extends StatelessWidget {{
  const {capitalizeName}({{super.key}});
  @override
  Widget build(BuildContext context) {{
    return const MaterialApp(
      home: Center(child: FlutterLogo()),
    );
  }}
}}
"""
mainFormat = {"capitalizeName": capitalizeName}
resMain = main.format(**mainFormat)

mainPath = "lib/main.dart"
mainDevPath = "lib/main_dev.dart"
mainSitPath = "lib/main_sit.dart"
mainUatPath = "lib/main_uat.dart"
mainProdPath = "lib/main_prod.dart"

# remove linux directory
shutil.rmtree(linuxPath)

# remove web directory
shutil.rmtree(webPath)

# remove windows directory
shutil.rmtree(windowsPath)

# remove mac os path
shutil.rmtree(macOSPath)

# replace main.dart with minimalist main and split to
# dev, sit, uat, prod
os.remove(mainPath);
fDev = open(mainDevPath, "a")
fSit = open(mainSitPath, "a")
fUat = open(mainUatPath, "a")
fProd = open(mainProdPath, "a")
fDev.write(resMain)
fDev.close()
fSit.write(resMain)
fSit.close()
fUat.write(resMain)
fUat.close()
fProd.write(resMain)
fProd.close()

# replace widget_test.dart with import from main_dev.dart
widgetTest= """
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:{appName}/main_dev.dart';

void main() {{
  testWidgets('Counter increments smoke test', (WidgetTester tester) async {{
    // Build our app and trigger a frame.
    await tester.pumpWidget(const {capitalizeName}());

    // Verify that our counter starts at 0.
    expect(find.text('0'), findsOneWidget);
    expect(find.text('1'), findsNothing);

    // Tap the '+' icon and trigger a frame.
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();

    // Verify that our counter has incremented.
    expect(find.text('0'), findsNothing);
    expect(find.text('1'), findsOneWidget);
  }});
}}
"""
widgetTestFormat = {"appName": name, "capitalizeName": capitalizeName}
resWidgetTestCode = widgetTest.format(**widgetTestFormat)

testPath = "test/widget_test.dart"
os.remove(testPath);

testDir = open(testPath, "a")
testDir.write(resWidgetTestCode)
testDir.close()


parent_dir = "./"
# create app dir
appDir = "lib/app"
appPath = os.path.join(parent_dir, appDir)
try:
  os.makedirs(appPath, exist_ok = True)
  print("Directory '%s' created successfully" % appDir)
except OSError as error:
    print("Directory '%s' can not be created" % appDir)

# create core dir
coreDir = "lib/app/core"
corePath = os.path.join(parent_dir, coreDir)
try:
  os.makedirs(corePath, exist_ok = True)
  print("Directory '%s' created successfully" % coreDir)
except OSError as error:
    print("Directory '%s' can not be created" % coreDir)


# create shared dir
sharedDir = "lib/app/shared"
sharedPath = os.path.join(parent_dir, sharedDir)
try:
  os.makedirs(sharedPath, exist_ok = True)
  print("Directory '%s' created successfully" % sharedDir)
except OSError as error:
    print("Directory '%s' can not be created" % sharedDir)


# create features dir
featuresDir = "lib/app/features"
featuresPath = os.path.join(parent_dir, featuresDir)
try:
  os.makedirs(featuresPath, exist_ok = True)
  print("Directory '%s' created successfully" % featuresDir)
except OSError as error:
    print("Directory '%s' can not be created" % featuresDir)

