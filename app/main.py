from utils import *
def main():
    # Them  config streamlit
    streamlit.set_page_config(layout='wide')

    # read the configuration file and initialize random generators
    cfg = read_config('/app/mib__analyse_app/app/config/config.yaml')

    # read dataframes
    df_termine, df_studenten, df_studentenxtermine, df_pk_stud = generate_dataframes(cfg)

    # Kurs Info
    # Kurs dataframe
    all_dates_kurse = df_termine[cfg['plots']['kurse']['fields']]

    # All courses
    all_courses_names = df_termine['MiB-Kurs-Name'].unique()

    # Options to select o sidebar
    kurs_selectbox = streamlit.sidebar.selectbox("Wählt kurs", all_courses_names)
    kurs_id = kurs_selectbox
    # Select value range for courses
    course_dates = all_dates_kurse[all_dates_kurse['MiB-Kurs-Name'] == kurs_selectbox]
    course_dates = course_dates['Datum-df']
    min_date_kurs, max_date_kurs = min_max_dates(course_dates)

    info_selection = streamlit.sidebar.radio("Wählt Info", ("Kurs Info", "Studenten Info"))

    # Decide which elements are going to be shown on the main page
    if info_selection == "Kurs Info":
        # Courses page
        streamlit.markdown("# Kurs Daten")

        # Streamlit visual
        streamlit.write(f'Hier sind die Infos zum {kurs_id}')

        col_date_1, col_date_2 = streamlit.columns(2)
        with col_date_1:
            start_date_kurs = streamlit.date_input('Anfangsdatum', min_value=min_date_kurs,
                                                   max_value=max_date_kurs, value=min_date_kurs)
        with col_date_2:
            end_date_kurs = streamlit.date_input('Enddatum', min_value=min_date_kurs,
                                                 max_value=max_date_kurs, value=max_date_kurs)

        # plot student info

        plot_kurs_data(df_termine, df_pk_stud, cfg, kurs_id,  start_date_kurs, end_date_kurs)

        # Tables

    else:
        streamlit.markdown("# Studenten Daten")

        # Streamlit visual
        streamlit.write(f'Hier stehen alle infos zu die Studenten aus dem {kurs_id}')

        # Student Info
        # Student dataframe
        all_dates_students = df_studentenxtermine[cfg['plots']['students']['fields']]
        all_dates_students = all_dates_students[all_dates_students['MiB-Kurs-Name'] == kurs_id]

        col_date_1, col_date_2 = streamlit.columns(2)
        with col_date_1:
            start_date = streamlit.date_input('Anfangsdatum', min_value=min_date_kurs,
                                              max_value=max_date_kurs, value=min_date_kurs)
        with col_date_2:
            end_date = streamlit.date_input('Enddatum', min_value=min_date_kurs,
                                            max_value=max_date_kurs, value=max_date_kurs)

        # Student selection
        students = streamlit.selectbox('Student ID', all_dates_students['MiB-ID'].unique())
        mib_id = students
        plot_student_data(df_studentenxtermine,df_pk_stud, cfg, mib_id, start_date, end_date)


if __name__ == "__main__":
    main()

