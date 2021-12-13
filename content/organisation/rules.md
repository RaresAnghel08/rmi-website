---
title: "Competition Rules"
menu:
  main:
    parent: "organisation"
    weight: 2
no_header: false
---

### Foreword

Because of the still ongoing COVID-19 pandemic, RMI 2021 will again be run as an online competition. As such, this year's edition largely keeps the requirements for proctoring the contestants and for the contest environments they use from last year's edition, which will be laid down in this document.

All times regarding the competition are going to be communicated in UTC time.


### Contest Sites

Students can participate in the contest from multiple contest sites.

A contest site can be either a room in a school, university, hotel, conference room etc, or a home.

A contest site can have one or more participants, provided that disease control safety rules and government regulations are followed.

It is important that the contest site provides a good internet connection.

Every contest site should have the following:
* One computer for each participant. Hardware and software requirements can be found in a later section. Spares are highly recommended in case of failure.
* Equipment for the proctor to engage in a video call (preferred) or a text chat with the organizing team in case of problems:
  * Camera setup that allows showing the participant (e.g. laptop camera, smartphone camera, external webcam)
  * Audio setup (microphone, speakers, headset) to communicate on the video call. Video call participants must be visible at all times.
* Ability to record and store footage of the contest site, showing all participants, and the screens of contestants' PCs for at least 30 days after the end of the contest. The footage should be provided in case of appeals. Details are written below.

Participants can bring snacks, food, and liquids. They can bring their own keyboard and mouse from home, only after disinfection and after being inspected by the proctor.

We recommend using network and power redundancy systems for the contest sites.


### Physical Proctoring

*Note: The following proctoring rules laid out in this section do not apply to teams from countries or regions where disease control rules do not allow it. See the section **Video Recording** for rules in this case.*

The team leader is responsible for enforcing these rules for their team(s). Every contestant is expected to be physically proctored by the team leader or by a person appointed by them.

The proctor must not be a relative of any of the proctored contestants.

The proctors for each contest site must be communicated before the first contest day of the competition (preparation day with systems check is not considered a contest day). *The list is going to be published on our website.*

Each contest site must have at least two proctors.

**Proctors must make sure that contestants don't do the following:**
* try to gain access to the root or administrator user
* try to establish communication with another system, via chat, remote shell or desktop sharing (Team Viewer, Anydesk, Remote Desktop, etc)
* try to attack the contest server


### Video Recording

Each contest site must be recorded for the entirety of the contest. Multiple feeds can be used from multiple angles for the same contest site.

The recordings must capture the faces of all contestants and the presence of at least one proctor.

We should be able to determine from the recordings whether contestants are at their computers and if there is a proctor in the room at all times.

**The screens of all contestants must also be recorded.** The recording must be of the full display, and the output video must have at least **5 frames per second** and **640 x 360 resolution**.

_**In countries or regions where proctoring is not possible, students must record their screen and themselves. You can record the screen with a screen recording program, and use a mobile phone to record yourself, for example.**_

For screen recording, you can use Kazam on Linux, or OBS Studio on Windows, macOS or Linux. This is only a recommendation.

If you use the virtual machine, you must **install the video recording software on the host system, outside the virtual machine**.

The use of multiple screens is not permitted, as outlined in **Computer Setup**. The recordings must only show a single monitor.


### Task Types

There are two types of tasks at RMI 2021:
* **Batch tasks:** solutions comprise a single source file of a computer program which reads data from the standard input and writes its answer to the standard output.
* **Manager tasks:** solutions comprise a single source file of a computer program which implements a number of functions. The program will be compiled and linked together with a manager program that calls these functions in a specified order. The Scientific Committee will provide the manager, which handles input and output and grades the solution.


### Computer Setup

**Contestants must use only one screen.**

**Usage of prewritten materials and code snippets (algorithms, data structures etc) is strictly prohibited.**

We provide a virtual machine to offer a consistent contest environment to all participants. It uses the same compiler version as the contest server and it includes many other debugging tools and text editors in a Linux-based system.

The virtual machine is **not required**, although you may use it to get an already configured Linux machine. It can be downloaded from the RMI 2021 website.

The virtual machine is **no longer required** in cases where proctoring is not possible due to disease control rules. The requirement for screen and room recordings **remains mandatory** in all scenarios. See **Video Recording** for details.

Because we are no longer in control of the hardware that the contestants use during the contest, the virtual machine is configured to snapshot the home directory of the contestant every 15 minutes to provide some fault tolerance. If you use the virtual machine, we advise you to be careful not to create very large files (tens of gigabytes), as those may get caught in a snapshot and use the storage even after deletion.

Included software:
* XFCE Desktop Environment
* Firefox
* Evince document viewer
* XFCE Terminal, GNOME Terminal and Konsole
* tmux and byobu
* Code::Blocks, Emacs, Eclipse C++ Edition, Geany, Sublime Text 3, Vim and Neovim • Python 3 and Ruby
* GCC and G++ 7.5.0, GDB, DDD (Data Display Debugger), Valgrind
* GNU Make
* C++ Man Pages (C++ Reference can also be viewed from the contest server)

To run the virtual machine, you need:
* Virtual Box
* Virtualization technology enabled in the BIOS (can also be found under the names VT-x, VT-d, SVM, AMD-V)
* Intel or AMD 64 bit CPU with at least two cores and four threads
* At least 8GB of RAM
* At least 64GB of **free** storage.

If you choose to use the virtual machine, you must run the virtual machine in full screen or maximized mode during the contest. The virtual machine adapts its screen resolution to the size of the window automatically.

**For contestants who do not wish to use the virtual machine**, you **may not** use any other software than:
* any text editor / IDE *that doesn't access the Internet and doesn't provide code snippet completion with algorithms, data structures or other templates that may provide an unfair advantage (for example, an editor that inserts the code for a binary search when typing “bsearch” or any other keyword)*
* a web browser
* a file manager
* a document viewer
* a C/C++ compiler
* a debugger *(debugger interfaces, such as those provided by an IDE or external interfaces like DDD are allowed)*
* Valgrind
* a terminal with a multiplexer of your choice *(screen, tmux, byobu)*
* Python and Ruby (any version) to write helper scripts
* a build system of your choice *(GNU Make, meson, etc)*
* a calculator
* Linux standard utilities *(GNU Coreutils, GNU Binutils)*

Contestants may create their own virtual machines with their own software choices.


### Limits

For every task the following limits will be enforced on the contestants' submissions:
* Time limit: a limit on the total processor time the process may consume while solving a given input.
* Memory limit: a limit on the total amount of memory the process may have allocated at any moment. Note that this limit includes not only the variables, but also the executable code, global data, the stack etc. There is no separate limit on the stack size.
* Source size limit: no submitted program may exceed 50 kB in size.

All task-dependent limits will be announced in the problem statements.


### Competition Equipment and Environment

Contestants can either use the virtual machine or the system of the contest site directly. The contest server uses the following compiler:
* g++ version 7.5.0, compilation command (for the program abc.cpp):
  * `g++ -DEVAL -static -O2 -std=c++11 -o abc abc.cpp`


### Submitting Solutions
The contestants' submissions are evaluated by a contest system. The contest system consists of a contest server. The contestants will be able to run their solutions on the server using the test facility.

* Contestants submit solutions to the contest server via a web-based submission system running on that server. Each contestant will be assigned a username and a password for accessing the web application on the contest server.
* Submissions are evaluated on the server. The software environment on the server is as close as possible to the environment on the contestant virtual machines.
* The submission facility will accept C++ source files, verify that the program compiles and obeys the stated limits on program source size; the submission facility will then run the program on the task test cases (different from the ones given in the task description), enforcing the relevant run-time resource constraints, grade the solutions and report the results to the contestants.
* For each task full feedback will be enabled.
* For each task at most 20 submissions are allowed.
* A wait period of one minute will be enforced between submissions from the same contestant, for the same task.

The solution must terminate its execution normally in order to be graded. If the solution returns an error code different from zero, the contest system will consider that the solution had a runtime error and no points will be awarded for the corresponding test case.

It is the responsibility of the contestants to submit their solutions to the contest system before the contest is finished. We advise the contestants to reserve enough time before the end of the contest to make sure that all of their solutions are submitted.

Contestants are allowed to use the test interface of the contest system to run their submitted solutions on test data of their choice. However, due to technical reasons, there is no guarantee that the test interface works properly.

### Scoring

For each task the test data will be divided into groups, with each group containing one or more test inputs. A test input is solved correctly if the submitted program produces a correct output file within the enforced limits. A group is solved correctly if each of the inputs it contains is solved correctly.

Points are awarded only for correctly solved groups of inputs. If there are partial grading rules for the problem, then the score for an input group will be the lowest among the scores for the particular test inputs contained in the group.

**The score of a contestant for a task is the sum of the scores obtained for each group of this task. The score obtained for a group is the highest score obtained on this group by all contestant's submissions**


### Feedback

For all tasks full feedback will be enabled. Every time contestants submit a solution, they receive full feedback for that submission. Due to technical reasons, feedback is guaranteed (only) for submissions received until a time equal to `initial duration minus 30 minutes` has elapsed since the beginning of the competition. The Scientific Committee is bound to extend competition time to accommodate this rule.


### Clarification Requests

During the first hour of competition, contestants may submit questions concerning any ambiguities or items needing clarification in the competition tasks through the contest interface. All questions regarding the problems must be submitted via the competition server, expressed either in the contestant's native language or in English.

If required, delegation leaders will translate their contestants' questions into English after they are submitted and before they are sent to the Scientific Committee. The Scientific Committee will respond to every question submitted by the contestants. Contestants should phrase their questions so that a yes/no answer will be meaningful.

Questions will be answered with one of the following:
* **Yes**
* **No**
* **Answered in the task description (explicitly or implicitly):** The task description contains sufficient information. The contestant should read it again carefully.
* **Invalid question:** The question is not phrased so that a yes/no answer would be meaningful. The contestant is encouraged to rephrase the question.
* **No comment:** The contestant is asking for information that the Scientific Committee cannot give.

If contestants have questions or issues not related to the problems (e.g. computer or network problems, request for additional blank papers, etc), they should notify the staff in the contest room by raising their hand.


### Announcements

In case the Scientific Committee makes verbal announcements during the competition, these announcements will also be available on the Competition Server's web interface. These announcements will be in the English language only. The web interface also shows the official time remaining in the contest.


### Conduct of Contest

Submitted programs are not allowed to:
* use external libraries (e.g., crt, graph)
* access the network
* fork
* open and create files others than those specified in the task statement
* attack the system security or the grader
* execute other programs
* change file system permissions
* read file system information
* make system calls not related to solving the competition task

During the contest, contestants are not allowed to:
* access the network for anything other than communicating with the competition server
* communicate with persons other than RMI staff
* reveal their passwords
* intentionally damage or endanger any part of the competition environment
* use any printed materials and electronic devices brought by themselves with the exception of a keyboard, mouse, and computer. We recommend having a spare computer.

Attempting any of the above actions may result in disqualification.

On the competition days, contestants may not bring anything into the competition rooms, but:
* writing utensils
* blank paper
* simple wristwatches
* small mascots (see below)
* English dictionaries (see below)

The team leader is responsible for checking the small mascots and English dictionaries, should the contestant want to bring any in the contest room.

Any attempt to bring any other item into the competition room will be considered cheating. In particular, during competition rounds it is strictly prohibited to bring any computing or communication devices or printed materials.

During the contest analysis, contestants are free to bring and use anything.


### Appeal Process

At the end of each competition day, submitted solutions are judged using data which conforms to the specifications given in the problem statement, but which is unknown to contestants during the competition.

A Team Leader may file an appeal to the Scientific Committee before 14:00 UTC in the afternoon of the same day.

Every appeal will be reviewed by the Scientific Committee and the team leader will be notified about the committee's decision.

In the event that a mistake is discovered in the grading of a task, the mistake will be corrected and the submissions of all contestants will be re-graded and re-scored, whether or not the scoring of that particular submission has been appealed. Note that re-scoring may result in a higher or lower score for any contestant. Should anyone's score change after grading results have been distributed, new results will be printed and distributed to them.


### Medal Allocation

After the second Competition Day and before the RMI Awards Ceremony the medal distribution is determined by an automatic procedure, based on the number of points the contestants achieved. The medal allocation is decided by the Scientific Committee and satisfies the following rules:
1. The score necessary to achieve a gold medal is the highest score such that at least one twelfth of all contestants receive a gold medal.
2. The score necessary to achieve a silver medal is the highest score such that at least one fourth of all contestants receive a silver or a gold medal.
3. The score necessary to achieve a bronze medal is the highest score such that at least one half of all contestants receive a medal.

Each team's score will be calculated as the sum of the best three scores of its members. The final standings will be posted on the official website and the team with the highest score will be awarded the RMI Cup.

Special awards may be distributed according to the will of the Scientific Committee in order to recognize outstanding performances.

