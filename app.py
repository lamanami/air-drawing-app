import os
import subprocess
import sys
import random
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Air Doodle Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# CUTE PROMPTS
# =========================================================

cute_messages = [
    "draw something silly today ✨",
    "tiny doodles count too 🌷",
    "your finger is basically a magic paintbrush 💫",
    "make something weird and cute 🎀",
    "doodle first, overthink later 💌",
    "draw the first thing that pops into your head ☁️",
]

today_message = random.choice(cute_messages)


# =========================================================
# CSS
# =========================================================

st.html(
    """
    <style>

    /* =====================================================
       HIDE STREAMLIT HEADER
    ===================================================== */

    [data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    header {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }


    /* =====================================================
       PAGE BACKGROUND
    ===================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    .stApp {

        background:

            radial-gradient(
                circle at 8% 10%,
                rgba(255, 205, 226, 0.85) 0px,
                rgba(255, 205, 226, 0.28) 250px,
                transparent 450px
            ),

            radial-gradient(
                circle at 92% 8%,
                rgba(220, 208, 255, 0.90) 0px,
                rgba(220, 208, 255, 0.25) 260px,
                transparent 460px
            ),

            radial-gradient(
                circle at 88% 80%,
                rgba(255, 239, 177, 0.72) 0px,
                rgba(255, 239, 177, 0.18) 240px,
                transparent 430px
            ),

            radial-gradient(
                circle at 8% 88%,
                rgba(205, 235, 255, 0.75) 0px,
                rgba(205, 235, 255, 0.18) 250px,
                transparent 450px
            ),

            linear-gradient(
                135deg,
                #fff9fb 0%,
                #fff3f8 30%,
                #f7f1ff 58%,
                #f3f9ff 78%,
                #fffaf1 100%
            ) !important;

        background-attachment: fixed !important;
    }


    /* =====================================================
       MAIN CONTAINER
    ===================================================== */

    .block-container {
        max-width: 1150px;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }


    /* =====================================================
       HERO
    ===================================================== */

    .hero {

        background: rgba(255, 253, 249, 0.88);

        border: 2px solid #4b3c46;

        border-radius: 32px;

        padding: 38px;

        margin-bottom: 42px;

        box-shadow:
            8px 8px 0 #f6bfd7,
            11px 11px 0 #4b3c46;

        position: relative;

        overflow: hidden;
    }


    .hero-badge {

        display: inline-block;

        background: #fff0ad;

        border: 2px solid #4b3c46;

        border-radius: 999px;

        padding: 7px 14px;

        font-weight: 850;

        margin-bottom: 20px;

        transform: rotate(-2deg);

        box-shadow: 2px 2px 0 #4b3c46;
    }


    .hero-title {

        font-size: clamp(2.7rem, 5vw, 4rem);

        font-weight: 950;

        line-height: 1;

        color: #4b3c46;

        margin-bottom: 15px;

        letter-spacing: -2px;
    }


    .hero-sub {

        color: #7a6874;

        font-size: 1.05rem;

        max-width: 700px;

        line-height: 1.75;
    }


    .sparkle {

        position: absolute;

        right: 50px;

        top: 32px;

        font-size: 4.8rem;

        opacity: 0.82;

        transform: rotate(10deg);
    }


    /* =====================================================
       SECTION TITLES
    ===================================================== */

    .section-title {

        font-size: 1.65rem;

        font-weight: 950;

        color: #4b3c46;

        margin-bottom: 7px;
    }


    .section-sub {

        color: #806f7b;

        font-size: 0.96rem;

        margin-bottom: 18px;
    }


    /* =====================================================
       COLOR PICKER
    ===================================================== */

    div[data-testid="stColorPicker"] {

        width: 100% !important;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.92),
                rgba(255,240,248,0.86)
            );

        border: 2px dashed #c5b0bf;

        border-radius: 26px;

        padding: 22px !important;

        box-sizing: border-box;

        min-height: 135px;

        box-shadow:
            4px 4px 0 rgba(75,60,70,0.10);
    }


    div[data-testid="stColorPicker"] > div {
        width: 100% !important;
    }


    div[data-testid="stColorPicker"] button {

        width: 100% !important;

        min-height: 72px !important;

        border-radius: 18px !important;

        border: 2px solid #4b3c46 !important;

        box-shadow: none !important;
    }


    div[data-testid="stColorPicker"] label {

        color: #4b3c46 !important;

        font-weight: 800 !important;
    }


    /* =====================================================
       GENERAL BUTTONS
    ===================================================== */

    .stButton > button {

        width: 100%;

        border-radius: 999px !important;

        border: 2px solid #4b3c46 !important;

        background:
            linear-gradient(
                90deg,
                #f6bfd7,
                #efc8ed
            ) !important;

        color: #4b3c46 !important;

        font-weight: 900 !important;

        font-size: 1rem !important;

        padding: 0.88rem 1rem !important;

        box-shadow:
            5px 5px 0 #4b3c46 !important;

        transition: 0.15s ease !important;
    }


    .stButton > button:hover {

        transform: translate(-2px, -2px);

        box-shadow:
            7px 7px 0 #4b3c46 !important;

        background:
            linear-gradient(
                90deg,
                #f4abc9,
                #e9bdea
            ) !important;
    }


    /* =====================================================
       GESTURE CARD
    ===================================================== */

    .gesture-box {

        background:
            linear-gradient(
                145deg,
                rgba(243, 236, 255, 0.96),
                rgba(253, 244, 255, 0.92)
            );

        border: 2px solid #4b3c46;

        border-radius: 25px;

        padding: 20px 22px;

        box-shadow:
            5px 5px 0 #4b3c46;
    }


    .gesture-row {

        display: flex;

        justify-content: space-between;

        align-items: center;

        padding: 12px 2px;

        border-bottom:
            1px dashed #baa9b6;

        gap: 20px;
    }


    .gesture-row:last-child {
        border-bottom: none;
    }


    .gesture-left {

        font-weight: 850;

        color: #4b3c46;
    }


    .gesture-right {

        color: #806f7b;

        font-weight: 650;
    }


    /* =====================================================
       PROMPT CARD
    ===================================================== */

    .vibe-card {

        background:
            linear-gradient(
                100deg,
                #fff1af,
                #ffe3c2,
                #ffdceb
            );

        border: 2px solid #4b3c46;

        border-radius: 22px;

        padding: 19px;

        box-shadow:
            4px 4px 0 #4b3c46;

        font-weight: 850;

        color: #4b3c46;

        text-align: center;

        margin-top: 26px;
    }


    /* =====================================================
       GALLERY
    ===================================================== */

    .gallery-note {

        color: #887781;

        margin-bottom: 16px;
    }


    div[data-testid="stImage"] img {

        border-radius: 22px;

        border: 2px solid #4b3c46;

        box-shadow:
            5px 5px 0 #f6bfd7;
    }


    .empty {

        text-align: center;

        border: 2px dashed #c9b8c4;

        border-radius: 26px;

        padding: 45px;

        color: #8d7d88;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.68),
                rgba(255,238,247,0.56)
            );
    }


    /* =====================================================
       DELETE ICON
    ===================================================== */

    div[data-testid="stPopover"] {

        margin-bottom: -3px !important;
    }


    div[data-testid="stPopover"] button {

        width: 34px !important;

        min-width: 34px !important;

        height: 34px !important;

        min-height: 34px !important;

        padding: 0 !important;

        border-radius: 50% !important;

        background:
            rgba(255,255,255,0.95) !important;

        border:
            1.5px solid #4b3c46 !important;

        box-shadow:
            2px 2px 0 #4b3c46 !important;

        font-size: 0.82rem !important;
    }


    div[data-testid="stPopover"] button:hover {

        background:
            #ffe5ef !important;

        transform:
            translate(-1px, -1px);

        box-shadow:
            3px 3px 0 #4b3c46 !important;
    }


    /* =====================================================
       ALERTS
    ===================================================== */

    div[data-testid="stAlert"] {

        border-radius: 18px !important;

        border:
            1.5px solid #4b3c46 !important;
    }


    /* =====================================================
       MOBILE
    ===================================================== */

    @media (max-width: 700px) {

        .hero {
            padding: 28px 24px;
        }

        .hero-title {
            font-size: 2.7rem;
        }

        .sparkle {
            display: none;
        }

    }

    </style>
    """
)


# =========================================================
# HERO
# =========================================================

st.html(
    """
    <div class="hero">

        <div class="hero-badge">
            ✿ hand-tracked doodles
        </div>

        <div class="hero-title">
            Air Doodle Studio 🎨
        </div>

        <div class="hero-sub">
            Pick a color, launch the camera, and draw in the air
            using your fingertip. Save your cutest creations and
            collect them in your little doodle shelf below.
        </div>

        <div class="sparkle">
            ✦
        </div>

    </div>
    """
)


# =========================================================
# TOP SECTION
# =========================================================

left, right = st.columns(
    [1.05, 0.95],
    gap="large",
)


# =========================================================
# LEFT — CAMERA
# =========================================================

with left:

    st.html(
        """
        <div class="section-title">
            Start a new doodle 🎀
        </div>

        <div class="section-sub">
            Pick your color first, then launch the camera.
        </div>
        """
    )


    selected_color = st.color_picker(
        "Choose your doodle color 🎨",
        "#F6BFD7",
    )


    st.write("")


    if st.button(
        "Launch camera ✨",
        use_container_width=True,
    ):

        subprocess.Popen(
            [
                sys.executable,
                "camera_draw.py",
                selected_color,
            ]
        )

        st.success(
            "Camera launched! Have fun doodling 💕"
        )


# =========================================================
# RIGHT — GESTURES
# =========================================================

with right:

    st.html(
        """
        <div class="section-title">
            Gesture cheat sheet ✋
        </div>

        <div class="section-sub">
            Your hand is the control panel.
        </div>


        <div class="gesture-box">

            <div class="gesture-row">
                <div class="gesture-left">
                    ☝️ Index finger
                </div>

                <div class="gesture-right">
                    Draw
                </div>
            </div>


            <div class="gesture-row">
                <div class="gesture-left">
                    ✌️ Two fingers
                </div>

                <div class="gesture-right">
                    Pause
                </div>
            </div>


            <div class="gesture-row">
                <div class="gesture-left">
                    ✋ Open palm
                </div>

                <div class="gesture-right">
                    Clear
                </div>
            </div>


            <div class="gesture-row">
                <div class="gesture-left">
                    👍 Thumbs up
                </div>

                <div class="gesture-right">
                    Save photo
                </div>
            </div>


            <div class="gesture-row">
                <div class="gesture-left">
                    Q
                </div>

                <div class="gesture-right">
                    Close camera
                </div>
            </div>

        </div>
        """
    )


# =========================================================
# DOODLE PROMPT
# =========================================================

st.write("")

st.html(
    f"""
    <div class="vibe-card">
        ✨ today's doodle prompt: {today_message}
    </div>
    """
)


# =========================================================
# GALLERY HEADER
# =========================================================

st.write("")
st.write("")

st.html(
    """
    <div class="section-title">
        Doodle Shelf 🖼️
    </div>

    <div class="gallery-note">
        Your latest saved Air Doodle pictures live here.
    </div>
    """
)


# =========================================================
# FIND SAVED IMAGES
# =========================================================

os.makedirs(
    "output",
    exist_ok=True,
)


saved_images = [

    os.path.join(
        "output",
        filename,
    )

    for filename in os.listdir(
        "output"
    )

    if filename.lower().endswith(
        (
            ".png",
            ".jpg",
            ".jpeg",
        )
    )
]


saved_images.sort(
    key=os.path.getmtime,
    reverse=True,
)


# =========================================================
# REFRESH + COUNT
# =========================================================

refresh_col, count_col = st.columns(
    [0.28, 0.72]
)


with refresh_col:

    if st.button(
        "Refresh shelf ↻",
        use_container_width=True,
    ):

        st.rerun()


with count_col:

    if saved_images:

        st.caption(
            f"{len(saved_images)} saved doodle"
            + (
                ""
                if len(saved_images) == 1
                else "s"
            )
        )


# =========================================================
# GALLERY STATE
# =========================================================

if "gallery_limit" not in st.session_state:

    st.session_state.gallery_limit = 9


# =========================================================
# GALLERY
# =========================================================

if not saved_images:

    st.html(
        """
        <div class="empty">

            <div style="font-size: 2.5rem;">
                🎨
            </div>

            <br>

            Your doodle shelf is empty for now.

            <br>

            Save a photo with a thumbs-up
            and it will appear here.

        </div>
        """
    )


else:

    gallery_images = saved_images[
        :st.session_state.gallery_limit
    ]


    gallery_columns = st.columns(
        3,
        gap="large",
    )


    for i, image_path in enumerate(
        gallery_images
    ):

        with gallery_columns[
            i % 3
        ]:

            filename = os.path.basename(
                image_path
            )


            # =================================================
            # DELETE ICON ROW
            # =================================================

            empty_space, delete_col = st.columns(
                [0.89, 0.11],
                gap="small",
            )


            with delete_col:

                with st.popover(
                    "🗑️",
                    use_container_width=True,
                ):

                    st.markdown(
                        "**Delete this doodle?**"
                    )

                    st.caption(
                        "This can't be undone."
                    )


                    if st.button(
                        "Yes, delete",
                        key=f"confirm_delete_{filename}",
                        use_container_width=True,
                    ):

                        try:

                            os.remove(
                                image_path
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Couldn't delete: {e}"
                            )


                    if st.button(
                        "Keep it 💕",
                        key=f"cancel_delete_{filename}",
                        use_container_width=True,
                    ):

                        st.rerun()


            # =================================================
            # IMAGE
            # =================================================

            st.image(
                image_path,
                use_container_width=True,
            )


    # =====================================================
    # SHOW MORE / SHOW LESS
    # =====================================================

    st.write("")


    show_more_col, show_less_col = st.columns(
        2,
        gap="medium",
    )


    if (
        st.session_state.gallery_limit
        <
        len(saved_images)
    ):

        with show_more_col:

            if st.button(
                "Show more ✨",
                key="show_more_gallery",
                use_container_width=True,
            ):

                st.session_state.gallery_limit += 9

                st.rerun()


    if (
        st.session_state.gallery_limit
        > 9
    ):

        with show_less_col:

            if st.button(
                "Show less ↑",
                key="show_less_gallery",
                use_container_width=True,
            ):

                st.session_state.gallery_limit = 9

                st.rerun()