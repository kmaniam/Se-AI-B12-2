import streamlit as st

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Calculator")


# --------------------------------------------------
# Initialize calculator state
# --------------------------------------------------

if "display" not in st.session_state:
    st.session_state.display = "0"

if "first_number" not in st.session_state:
    st.session_state.first_number = None

if "operator" not in st.session_state:
    st.session_state.operator = None

if "new_number" not in st.session_state:
    st.session_state.new_number = True


# --------------------------------------------------
# Number function
# --------------------------------------------------

def number_click(number):

    if st.session_state.new_number:
        st.session_state.display = str(number)
        st.session_state.new_number = False

    else:
        if st.session_state.display == "0":
            st.session_state.display = str(number)
        else:
            st.session_state.display += str(number)


# --------------------------------------------------
# Decimal function
# --------------------------------------------------

def decimal_click():

    if st.session_state.new_number:
        st.session_state.display = "0."
        st.session_state.new_number = False

    elif "." not in st.session_state.display:
        st.session_state.display += "."


# --------------------------------------------------
# Operator function
# --------------------------------------------------

def operator_click(operator):

    try:
        st.session_state.first_number = float(
            st.session_state.display
        )

        st.session_state.operator = operator
        st.session_state.new_number = True

    except ValueError:
        st.session_state.display = "Error"


# --------------------------------------------------
# Calculate function
# --------------------------------------------------

def calculate():

    # Check whether an operation was selected
    if st.session_state.first_number is None:
        return

    if st.session_state.operator is None:
        return

    try:

        second_number = float(
            st.session_state.display
        )

        first_number = st.session_state.first_number

        operator = st.session_state.operator

        # Addition
        if operator == "+":
            result = first_number + second_number

        # Subtraction
        elif operator == "-":
            result = first_number - second_number

        # Multiplication
        elif operator == "×":
            result = first_number * second_number

        # Division
        elif operator == "÷":

            if second_number == 0:
                st.session_state.display = "Error"
                st.session_state.first_number = None
                st.session_state.operator = None
                return

            result = first_number / second_number

        else:
            return

        # Remove .0 for whole numbers
        if result == int(result):
            result = int(result)

        st.session_state.display = str(result)

        # Reset operation
        st.session_state.first_number = None
        st.session_state.operator = None
        st.session_state.new_number = True

    except Exception:
        st.session_state.display = "Error"


# --------------------------------------------------
# Clear function
# --------------------------------------------------

def clear_calculator():

    st.session_state.display = "0"
    st.session_state.first_number = None
    st.session_state.operator = None
    st.session_state.new_number = True


# --------------------------------------------------
# Display
# --------------------------------------------------

st.text_input(
    "Display",
    value=st.session_state.display,
    disabled=True
)


st.write("")


# --------------------------------------------------
# Calculator buttons
# Numbers = Left
# Operators = Right
# --------------------------------------------------


# ==========================
# Row 1
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button(
        "7",
        use_container_width=True,
        on_click=number_click,
        args=(7,)
    )

with col2:
    st.button(
        "8",
        use_container_width=True,
        on_click=number_click,
        args=(8,)
    )

with col3:
    st.button(
        "9",
        use_container_width=True,
        on_click=number_click,
        args=(9,)
    )

with col4:
    st.button(
        "÷",
        use_container_width=True,
        on_click=operator_click,
        args=("÷",)
    )


# ==========================
# Row 2
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button(
        "4",
        use_container_width=True,
        on_click=number_click,
        args=(4,)
    )

with col2:
    st.button(
        "5",
        use_container_width=True,
        on_click=number_click,
        args=(5,)
    )

with col3:
    st.button(
        "6",
        use_container_width=True,
        on_click=number_click,
        args=(6,)
    )

with col4:
    st.button(
        "×",
        use_container_width=True,
        on_click=operator_click,
        args=("×",)
    )


# ==========================
# Row 3
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button(
        "1",
        use_container_width=True,
        on_click=number_click,
        args=(1,)
    )

with col2:
    st.button(
        "2",
        use_container_width=True,
        on_click=number_click,
        args=(2,)
    )

with col3:
    st.button(
        "3",
        use_container_width=True,
        on_click=number_click,
        args=(3,)
    )

with col4:
    st.button(
        "-",
        use_container_width=True,
        on_click=operator_click,
        args=("-",)
    )


# ==========================
# Row 4
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button(
        "0",
        use_container_width=True,
        on_click=number_click,
        args=(0,)
    )

with col2:
    st.button(
        "00",
        use_container_width=True,
        on_click=number_click,
        args=(0,)
    )

with col3:
    st.button(
        ".",
        use_container_width=True,
        on_click=decimal_click
    )

with col4:
    st.button(
        "+",
        use_container_width=True,
        on_click=operator_click,
        args=("+",)
    )


# ==========================
# Row 5
# ==========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button(
        "AC",
        use_container_width=True,
        on_click=clear_calculator
    )

with col2:
    st.button(
        "=",
        use_container_width=True,
        on_click=calculate
    )