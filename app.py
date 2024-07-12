# import streamlit as st
from Sniper import Sniper
import threading
import datetime

# Set up logging


def main():
    # st.header("Sniper")

    # input_index = st.text_input("Input a index number")
    # st.empty()
    # if input_index:
    sniper = Sniper()
    sniper.setEmail(
        "rutgersnbsniper@gmail.com",
        "woff flkn kgyu dwre",
        [
            "ruthvikatte24@gmail.com",
            "atte.ruthvik@gmail.com",
            "atte.srinivas@gmail.com",
        ],
    )

    # while True:
    #     print(sniper.getNumThreads())
    #     x = input("Input and Index press x to end snipes y to show all snipes: ")
    #     if x == "x":
    #         y = input("Input index you want to stop: ")
    #         sniper.deleteSnipe(y)

    #     elif x == "y":
    #         print(sniper.showRunningSnipes())
    #     else:
    #         sniper.addSnipe([x])

    sniper.addSnipe(
        [
            # "18303",
            # "18306",
            # "07609",
            # "07610",
            # "07611",
            # "07612",
            # "07613",
            # "07614",
            # "07615",
            # "07616",
            # "09622",
            "07474",
            "07485",
        ]
    )


if __name__ == "__main__":
    main()


# currentlySxniping =
