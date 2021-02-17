import tableauserverclient as TSC
import logging


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level="NOTSET")

server = TSC.Server("http://cshin", use_server_version=True)
auth = TSC.TableauAuth('testadmin', '123', site='')
# auth = TSC.PersonalAccessTokenAuth("token", "KGazklZjSci8W+jRIiNGlQ==:quXIS9lwBPBKKyyGW4tdC5PBFxJRBBOR", site_id='')

with server.auth.sign_in(auth):

    tasks, _ = server.tasks.get(task_type=TSC.TaskItem.Type.ExtractRefresh)

    print(tasks[0].__dict__)

    # gp = TSC.GroupItem("Automation", "tsi.lan")
    # gp.minimum_site_role = TSC.UserItem.Roles.SiteAdministratorExplorer
    # gp.license_mode = TSC.GroupItem.LicenseMode.onSync

    # gp = server.groups.create_AD_group(gp)

    # print(gp.__dict__)

    # gp.name = "adGroupTestUsers"
    # gp.minimum_site_role = TSC.UserItem.Roles.ExplorerCanPublish
    # gp.license_mode = TSC.GroupItem.LicenseMode.onLogin

    # gp = server.groups.update(gp)

    # print(gp.__dict__)

    # server.groups.update(gp, as_job=True)

    # wb = TSC.WorkbookItem('', name='Samples')

    # file = open('./YoutubeSample.twbx', 'rb')
    # wb = server.workbooks.publish(wb, file, TSC.Server.PublishMode.Overwrite)
    #
    # wb = server.workbooks.publish(wb, './YoutubeSample.twbx', TSC.Server.PublishMode.Overwrite)
    # print(wb)


    # all_users, _ = server.users.get()
    # TSC.DatasourceItem.AskDataEnablement.Enabled

    # print(all_users[0].__dict__)
    # server.datasources.publish(ds, './Economy.tdsx', TSC.Server.PublishMode.Overwrite)


    # print(len(wbs))

