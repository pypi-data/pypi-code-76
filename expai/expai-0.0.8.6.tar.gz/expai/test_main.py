from expai.expai_requests import ExpaiLogin

if __name__ == '__main__':
    expaireq = ExpaiLogin(email="test@test.com", user_pass="test", api_key="6H19l-zXUzJVli2bcEMENssBjx0Ph4dnI0rmNtWcVac")
    projects = expaireq.project_list(search_by='Proy')
    project = expaireq.get_project(project_name='Proyecto 1')
    test = project.create_sample(sample_path='/Users/javi/Desktop/subir1.csv',
                          sample_name="Sample prueba lista5", sample_separator=",", is_display=False)
    project.append_sample(sample_path='/Users/javi/Desktop/subir2.csv',
                          sample_name="Sample prueba lista5")

    probando = project.get_sample(sample_name="Sample prueba lista5")
    projects = expaireq.project_list(exact_search='Proyecto 1')
    projects = expaireq.project_list(exact_search='Proyec 1')
    response = expaireq.delete_project(project_name="Prueba pycharm 2")
    #response = expaireq.create_project("Prueba pycharm 2")
    project = expaireq.get_project(project_name='Explanation test')
    project.create_sample(sample_path='/Users/javi/Desktop/Trabajo/Expai/expai/test/propension/X.csv',
                          sample_name="Sample 1", sample_separator=",", sample_target_col='y')
    project.create_model("/Users/javi/Desktop/Trabajo/Expai/expai/test/propension/model.pkl", True, "Model 1")
    explainer = project.get_model_explainer(model_name="Test model")
    shap_values = explainer.raw_explanation(sample_name="primera prueba con target aaaa", indexes=[0, 1])
    print(response)

