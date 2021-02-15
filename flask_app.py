from flask import Flask, render_template, request
import dropbox
import io
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

token = "---" # <---------- ENTER TOKEN HERE
sheet_names = ['Essence', 'Strengths','Dreams','Design']


def error_page(text):
    return render_template("error.html", error_text=text)


def create_dbx():
    if 'dbx' not in globals():
        try:
            global dbx
            dbx = dropbox.Dropbox(token) # TODO: will still create instance when token is wrong, fix
            success = True
        except:
            success = False
        finally:
            return success

    return True # dbx already exists


# gets "about appreciative inquiry" blurb for top of page
def get_blurb():
    filename = "blurb.txt"
    filepath = "/{}".format(filename)

    try:
        _, res = dbx.files_download(filepath)
        res.raise_for_status()
        with io.BytesIO(res.content) as stream:
            blurb = stream.read().decode()
    except:
        blurb = get_fallback_blurb()

    return blurb


def get_fallback_blurb():
    blurb = "The tree represents a story of wholeness and the cyclic nature of appreciative inquiry.  As the essence of the ground provides nourishment to feed the growing tree, the tree itself is anchored by the strengths of the trunk.  The branches that reach upwards towards the dreams (represented by clouds) provide places for leaves of action to shoot from.  As leaves realise their potential, their life cycle brings them back to the ground, where they feed back into the essence, and become fertiliser for the cycle to repeat itself and grow the tree further toward its dreams. The image below represents the story that emerged from this group.  While this image represents themes from the day in an easily digestible form, it is only the surface of a much richer set of stories, values, and emotions that were shared between people on the day."
    return blurb


#gets a list of all folders in root directory
def get_folder_names():
    folder_names = []

    try:
        folders = dbx.files_list_folder('')

        for folder in folders.entries:
            if isinstance(folder, dropbox.files.FolderMetadata) and get_xls_in_folder(folder.name) is not None: #check excel files in folder
                folder_names.append(folder.name)
    except:
        error_page("Error retrieving folders from Dropbox.")

    return folder_names


def folder_exists(find_me):
    found = False
    for folder_name in get_folder_names():
        if folder_name == find_me:
            found = True

    return found


#gets the first .xls* file within a given folder
def get_xls_in_folder(folder_name):
    files = dbx.files_list_folder('/{}'.format(folder_name))
    excel_extensions = (".xlsx", ".xlsm",".xls")

    for file in files.entries:
        if file.name.lower().endswith(excel_extensions):
            return file.name

    return None


# TODO: image format validation
def get_image_links(folder_name):
    info = dbx.sharing_list_shared_links()
    meta = info.links # link to Dropbox file preview page

    links_list = []
    for link in meta: # alter url to point to image directly (not Dropbox preview page) 
        if link.path_lower.find(folder_name.lower()) != -1:
            img_url = link.url
            img_url = img_url.replace("dl=0","raw=1")
            links_list.append(img_url)

    return links_list


def read_data_into_df(folder_name, file_name):
    filepath = "/{}/{}".format(folder_name, file_name)

    try:
        _, res = dbx.files_download(filepath)

        all_data = pd.DataFrame()
        with io.BytesIO(res.content) as stream:
            for sheet in sheet_names:
                df = pd.read_excel(stream, sheet_name=sheet, usecols="A:B")
                df['Phase'] = sheet
                all_data = all_data.append(df, ignore_index=True)

        return all_data
    except:
        error_page("Error reading data.")


def df_tidy(df):
    df = df.dropna(axis = 0,thresh = 2) #drop if 2+ columns empty - cannot drop all as phase is added to all rows
    df = df.fillna('')
    df = df.applymap(lambda s: s.capitalize() if type(s) == str else s) # capitalise first words only

    return df


def df_to_dict(df):
    df_tidy(df)
    full_dict = {}  # dict w phases as key

    for phase in df.Phase.unique():
        phase_df = df[df['Phase'] == phase]  # df for a single phase only
        phase_df = df_tidy(phase_df)
        temp_dict_themes = {}  # dict w themes as key

        for theme in phase_df.Themes.unique():
            theme_df = phase_df[phase_df['Themes'] == theme]  # df for a single theme only
            theme_df = df_tidy(theme_df)
            subthemes_list = theme_df['Raw data'].to_list()
            temp_dict_themes[theme] = subthemes_list

        full_dict[phase] = temp_dict_themes

    return full_dict


@app.route('/', methods=['GET'])
def landing_page():
    if not create_dbx():
        return render_template("error.html",error_text="Error connecting to Dropbox: token missing.")

    filenames = get_folder_names()
    return render_template("main_page.html",filenames=filenames)


@app.route('/forest', methods=['GET'])
def forest():
    if not create_dbx():
        return render_template("error.html",error_text="Error connecting to Dropbox: token missing.")

    folder_name = request.args.get('tree', type = str) # get folder name from url
    folder_name = folder_name.replace("%20", " ") # replace spaces
    filenames = get_folder_names()

    # find that filename in the dropbox, build tree or error page
    if folder_exists(folder_name):
        filename = get_xls_in_folder(folder_name)
        if filename == None:
            return render_template("error.html", error_text="Cannot find any excel files in the {} folder.".format(folder_name))
        else:
            full_dict = df_to_dict(read_data_into_df(folder_name,filename))
            blurb = get_blurb()
            return render_template("tree.html", full_dict=full_dict, filenames=filenames, blurb=blurb, img_url_list=get_image_links(folder_name))
    else:
        return render_template("tree_not_found.html", filenames=filenames)
