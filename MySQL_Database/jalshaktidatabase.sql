CREATE DATABASE  IF NOT EXISTS jalshaktimodels;

USE jalshaktimodels;

DROP TABLE IF EXISTS water_quality_testing;
DROP TABLE IF EXISTS VillageContamination;

CREATE TABLE water_quality_testing (
    S_No INT PRIMARY KEY,
    State_Name VARCHAR(255),
    Total_Sources INT,
    Sources_Tested INT,
    Sources_Yet_To_Be_Tested INT,
    Sources_Found_Safe INT,
    Sources_Found_Contaminated INT,
    Remedial_Measures_Taken INT
);

INSERT INTO water_quality_testing 
(S_No, State_Name, Total_Sources, Sources_Tested, Sources_Yet_To_Be_Tested, Sources_Found_Safe, Sources_Found_Contaminated, Remedial_Measures_Taken)
VALUES
(1, 'Andaman & Nicobar Islands', 178, 70, 108, 52, 18, 0),
(2, 'Andhra Pradesh', 146804, 145523, 1281, 143946, 1577, 1253),
(3, 'Arunachal Pradesh', 1035, 697, 338, 688, 9, 2),
(4, 'Assam', 101933, 89187, 12746, 87379, 1808, 981),
(5, 'Bihar', 106496, 37155, 69341,27911, 9244, 4613),
(6, 'Chhattisgarh', 64276, 58343, 5933, 57984, 359, 236),
(7, 'Goa', 113, 113, 0, 113, 0, 0),
(8, 'Gujarat', 71085, 53379, 17706, 45901, 7478, 5988),
(9, 'Haryana', 11694, 9114, 2580, 8244, 870, 536),
(10, 'Himachal Pradesh', 8543, 8428, 115, 8092, 336, 201),
(11, 'Jammu & Kashmir', 3274, 3214, 60, 3207, 7, 7),
(12, 'Jharkhand', 117024, 114395, 2629, 113868, 527, 256),
(13, 'Karnataka', 306530 ,280767, 257683,263440, 17327, 10589),
(14, 'Kerala', 2070, 1879, 191, 1192, 687, 295),
(15, 'Ladakh', 667, 514, 153, 476, 38, 12),
(16, 'Madhya Pradesh', 94198, 93945, 253, 93454, 491, 458),
(17, 'Maharashtra', 97669, 87148, 10521, 78637, 8511, 3115),
(18, 'Manipur', 148, 144, 4, 144, 0, 0),
(19, 'Meghalaya', 1089, 801, 288, 798, 3, 2),
(20, 'Mizoram', 81, 79, 2, 77, 2, 1),
(21, 'Nagaland', 693, 591, 102, 566, 25, 25),
(22, 'Odisha', 41813, 37769, 4044, 36664, 1105, 814),
(23, 'Puducherry', 526, 229, 297, 162, 67, 0),
(24, 'Punjab', 13555, 13539, 16, 12453, 1086, 985),
(25, 'Rajasthan', 38490, 33211, 5279, 29390, 3821, 1985),
(26, 'Sikkim', 40, 40, 0, 35, 5, 1),
(27, 'Tamil Nadu', 182583, 181340, 1243, 179943, 1397, 1379),
(28, 'Telangana', 90995, 40159, 50836, 40159, 0, 0),
(29, 'Tripura', 21750, 15453, 6297, 14765, 708, 684),
(30, 'Uttar Pradesh', 53634, 52890, 744, 51203, 1687, 886),
(31, 'Uttarakhand', 3985, 3753, 232, 3673, 80, 77),
(32, 'West Bengal', 18623, 5994, 12629, 3260, 2734, 1777);

CREATE TABLE VillageContamination (
    SNo INT PRIMARY KEY,
    State VARCHAR(255),
    pH INT,
    TDS INT,
    Turbidity INT,
    Chloride INT,
    Total_Alkalinity INT,
    Total_Hardness INT,
    Sulphate INT,
    Iron INT,
    Total_Arsenic INT,
    Fluoride INT,
    Nitrate INT,
    Residual_Chlorine INT,
    Others_Chemical INT,
    E_coli INT,
    Total_Coliform INT,
    Others_Bacteriological INT
);


INSERT INTO VillageContamination (SNo, State, pH, TDS, Turbidity, Chloride, Total_Alkalinity, Total_Hardness, Sulphate, Iron, Total_Arsenic, Fluoride, Nitrate, Residual_Chlorine, Others_Chemical, E_coli, Total_Coliform, Others_Bacteriological)
VALUES
(1, 'Andaman & Nicobar Islands', 3, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0),
(2, 'Andhra Pradesh', 5, 166, 12, 54, 62, 162, 5, 18, 0, 85, 29, 1, 12, 3, 14, 0),
(3, 'Arunachal Pradesh', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(4, 'Assam', 63, 0, 430, 0, 0, 0, 0, 779, 13, 2, 3, 0, 200, 170, 0, 58),
(5, 'Bihar', 43, 2, 49, 0, 1, 1, 0,1705, 67, 32, 0, 0, 1, 7, 0, 0),
(6, 'Chhattisgarh', 15, 0, 123, 0, 0, 7, 0, 46, 0, 34, 1, 0, 21, 0, 1, 0),
(7, 'Dadra & Nagar Haveli And Daman & Diu', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(8, 'Goa', 1, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(9, 'Gujarat', 31, 177, 97, 96, 94, 229, 30, 0, 0, 213, 605, 1, 184, 50, 64, 5),
(10, 'Haryana', 0, 74, 4, 19, 19, 72, 30, 3, 0, 88, 3, 0, 162, 0, 522, 0),
(11, 'Himachal Pradesh', 0, 0, 5, 0, 0, 0, 0, 4, 0, 0, 0, 1 , 5 , 2 , 4 , 0),
(12, 'Jammu & Kashmir', 2, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0,0, 8, 0, 9),
(13, 'Jharkhand',0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 3, 0),
(14, 'Karnataka', 111, 302, 266, 47, 275, 1358, 63, 74, 0, 730, 1409, 1, 637, 225, 569, 0),
(15, 'Kerala', 441, 11, 423, 5, 2, 5, 0, 163, 0, 15, 8, 47, 66, 447, 872, 0),
(16, 'Ladakh', 1, 0, 22, 0, 0, 1, 2, 0, 0, 0, 0, 1, 2, 0, 0, 0),
(17, 'Lakshadweep', 1, 3, 0, 3, 2, 4, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0),
(18, 'Madhya Pradesh', 41, 4, 46, 6, 11, 13, 0, 24, 5, 67, 40, 0, 6, 25, 40, 1),
(19, 'Maharashtra', 416, 303, 240, 42, 152, 1028, 92, 170, 0, 276, 3219, 0, 237, 2548, 4161, 0),
(20, 'Manipur', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
(21, 'Meghalaya', 2, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 8, 34, 0),
(22, 'Mizoram', 5, 0, 14, 0, 0, 0, 0, 1, 0, 0, 0 , 0 , 0, 98, 122, 0),
(23, 'Nagaland', 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0 , 0 , 0 , 0 , 0),
(24, 'Odisha', 22, 12, 594, 9, 9, 49, 1, 526, 1, 67, 318, 0, 56,0, 10, 0),
(25, 'Puducherry', 6, 1, 5, 1, 0, 3, 1, 7, 0, 1, 0, 0, 0 , 3 , 0 ,7),
(26, 'Punjab', 3, 0, 0, 0, 2, 2, 4, 0, 17, 13, 0, 0, 39, 0, 0 , 0),
(27, 'Rajasthan', 63, 1707, 7, 816, 694, 1089, 13, 2, 0, 1726, 2065, 5, 339, 0, 19, 0),
(28, 'Sikkim', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 26, 0),
(29, 'Tamil Nadu', 2, 2, 0, 1, 3, 2, 0, 2, 0 , 2 , 1, 1, 0, 0 , 1 , 0),
(30, 'Telangana', 0, 0, 0, 0 , 0 , 2, 0, 0, 0 , 1, 0, 0, 2, 0, 0, 0),
(31, 'Tripura', 0, 0, 18, 0, 0, 0, 0, 81, 0, 0, 0, 0, 0 , 0 , 0 , 0),
(32, 'Uttar Pradesh', 32, 55, 276, 15, 25, 62, 31, 37, 36, 37 , 83, 1 , 56 , 239, 282, 0),
(33, 'Uttarakhand', 8, 0, 6, 0 , 1, 2, 0, 0 , 0 , 0 , 0 , 0 , 1, 14, 19, 0),
(34, 'West Bengal', 0, 163, 10965, 45, 0, 481, 0, 9881, 2021, 120, 0, 60, 1384, 5589, 9918, 0);

