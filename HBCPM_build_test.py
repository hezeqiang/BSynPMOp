from HBCPM import HBCPMWrapper


if __name__ == "__main__":
    # Test the HBCPM model
    HBCPM = HBCPMWrapper()
    # you can choose either build a new project or resume a project

    # the .json file containing the para of the projrct you want to create
    filename ="8p12s_HBCPM_without_radial_PM_four_slot.json"
    HBCPM.create_project(filename)
    print("Project created")
    HBCPM.build_motor()
    HBCPM.mesh()
    HBCPM.create_relative_coordinate_system()
    HBCPM.assign_boudry_band()
    HBCPM.assign_force_torque()
    HBCPM.create_excitation()
    HBCPM.create_setup()
    HBCPM.create_report()
    HBCPM.analyze_torque()
    # HBCPM.analyze_force()
    HBCPM.release_project()


    # # the full path of the project you want to resume
    # prokect_name="C:/he/HBCPM/4p12s_HBCPM_with_radial_PM_four_slotProject_TZ8/Project_TZ8.aedt"
    # HBCPM.resume_project(project_name=prokect_name)
    # print("Project resumed")
    # print(HBCPM.HBCPM)
    # HBCPM.generate_mesh_export()
    # # HBCPM.analyze_torque()
    # HBCPM.analyze_force()
    # HBCPM.release_project()





