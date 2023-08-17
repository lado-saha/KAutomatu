from common import println, Status


def title_printer(speed: int = 0.0001):
    println("  ****************            *******      *******     ****************     ********************   ******        ******", Status.T_CYAN, speed)
    println("********************          ********    ********   ********************   ********************   ******        ******", Status.T_CYAN, speed)
    println("********************          ****** **  ** ******   ********************   ********************   ******        ******", Status.T_CYAN, speed)
    println("******        ******          ******  ****  ******   ******        ******         ********         ******        ******", Status.T_CYAN, speed)
    println("******        ******          ******   **   ******   ******        ******         ********         ******        ******", Status.T_BLUE, speed)
    println("******        ******  ******  ******        ******   ******        ******         ********         ******        ******", Status.T_BLUE, speed)
    println("********************  ******  ******        ******   ********************         ********         ******        ******", Status.T_BLUE, speed)
    println("********************  ******  ******        ******   ********************         ********         ******        ******", Status.T_BLUE, speed)
    println("******        ******          ******        ******   ******        ******         ********         ******        ******", Status.T_GREEN, speed)
    println("******        ******          ******        ******   ******        ******         ********         ********************", Status.T_GREEN, speed)
    println("******        ******          ******        ******   ******        ******         ********         ********************", Status.T_GREEN, speed)
    println("******        ******          ******        ******   ******        ******         ********           ****************  ", Status.T_GREEN, speed)



"""
def title_printer(speed: int = 0.0001):
    println("  ****************     ******        ******   ********************    *******************    *******      *******     ****************     ********************   ******        ******", Status.T_CYAN, speed)
    println("********************   ******        ******   ********************   *********************   ********    ********   ********************   ********************   ******        ******", Status.T_CYAN, speed)
    println("********************   ******        ******   ********************   *********************   ****** **  ** ******   ********************   ********************   ******        ******", Status.T_CYAN, speed)
    println("******        ******   ******        ******         ********         *******        ******   ******  ****  ******   ******        ******         ********         ******        ******", Status.T_CYAN, speed)
    println("******        ******   ******        ******         ********         *******        ******   ******   **   ******   ******        ******         ********         ******        ******", Status.T_BLUE, speed)
    println("******        ******   ******        ******         ********         *******        ******   ******        ******   ******        ******         ********         ******        ******", Status.T_BLUE, speed)
    println("********************   ******        ******         ********         *******        ******   ******        ******   ********************         ********         ******        ******", Status.T_BLUE, speed)
    println("********************   ******        ******         ********         *******        ******   ******        ******   ********************         ********         ******        ******", Status.T_BLUE, speed)
    println("******        ******   ******        ******         ********         *******        ******   ******        ******   ******        ******         ********         ******        ******", Status.T_GREEN, speed)
    println("******        ******   ********************         ********         *********************   ******        ******   ******        ******         ********         ********************", Status.T_GREEN, speed)
    println("******        ******   ********************         ********         *********************   ******        ******   ******        ******         ********         ********************", Status.T_GREEN, speed)
    println("******        ******     ****************           ********          *******************    ******        ******   ******        ******         ********           ****************  ", Status.T_GREEN, speed)
"""

"""


print("  AAAAAAAAAAAAAAAA     UUUUUU        UUUUUU   TTTTTTTTTTTTTTTTTTTT    OOOOOOOOOOOOOOOOOOO    MMMMMMM      MMMMMMM     AAAAAAAAAAAAAAAA     TTTTTTTTTTTTTTTTTTTT   UUUUUU        UUUUUU")
print("AAAAAAAAAAAAAAAAAAAA   UUUUUU        UUUUUU   TTTTTTTTTTTTTTTTTTTT   OOOOOOOOOOOOOOOOOOOOO   MMMMMMMM    MMMMMMMM   AAAAAAAAAAAAAAAAAAAA   TTTTTTTTTTTTTTTTTTTT   UUUUUU        UUUUUU")
print("AAAAAAAAAAAAAAAAAAAA   UUUUUU        UUUUUU   TTTTTTTTTTTTTTTTTTTT   OOOOOOOOOOOOOOOOOOOOO   MMMMMM MM  MM MMMMMM   AAAAAAAAAAAAAAAAAAAA   TTTTTTTTTTTTTTTTTTTT   UUUUUU        UUUUUU")
print("AAAAAA        AAAAAA   UUUUUU        UUUUUU         TTTTTTTT         OOOOOOO        OOOOOO   MMMMMM  MMMM  MMMMMM   AAAAAA        AAAAAA         TTTTTTTT         UUUUUU        UUUUUU")
print("AAAAAA        AAAAAA   UUUUUU        UUUUUU         TTTTTTTT         OOOOOOO        OOOOOO   MMMMMM   MM   MMMMMM   AAAAAA        AAAAAA         TTTTTTTT         UUUUUU        UUUUUU")
print("AAAAAA        AAAAAA   UUUUUU        UUUUUU         TTTTTTTT         OOOOOOO        OOOOOO   MMMMMM        MMMMMM   AAAAAA        AAAAAA         TTTTTTTT         UUUUUU        UUUUUU")
print("AAAAAAAAAAAAAAAAAAAA   UUUUUU        UUUUUU         TTTTTTTT         OOOOOOO        OOOOOO   MMMMMM        MMMMMM   AAAAAAAAAAAAAAAAAAAA         TTTTTTTT         UUUUUU        UUUUUU")
print("AAAAAAAAAAAAAAAAAAAA   UUUUUU        UUUUUU         TTTTTTTT         OOOOOOO        OOOOOO   MMMMMM        MMMMMM   AAAAAAAAAAAAAAAAAAAA         TTTTTTTT         UUUUUU        UUUUUU")
print("AAAAAA        AAAAAA   UUUUUU        UUUUUU         TTTTTTTT         OOOOOOO        OOOOOO   MMMMMM        MMMMMM   AAAAAA        AAAAAA         TTTTTTTT         UUUUUU        UUUUUU")
print("AAAAAA        AAAAAA   UUUUUUUUUUUUUUUUUUUU         TTTTTTTT         OOOOOOOOOOOOOOOOOOOOO   MMMMMM        MMMMMM   AAAAAA        AAAAAA         TTTTTTTT         UUUUUUUUUUUUUUUUUUUU")
print("AAAAAA        AAAAAA   UUUUUUUUUUUUUUUUUUUU         TTTTTTTT         OOOOOOOOOOOOOOOOOOOOO   MMMMMM        MMMMMM   AAAAAA        AAAAAA         TTTTTTTT         UUUUUUUUUUUUUUUUUUUU")
print("AAAAAA        AAAAAA     UUUUUUUUUUUUUUUU           TTTTTTTT          OOOOOOOOOOOOOOOOOOO    MMMMMM        MMMMMM   AAAAAA        AAAAAA         TTTTTTTT           UUUUUUUUUUUUUUUU  ")


"""

