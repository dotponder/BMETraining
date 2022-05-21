import pandas as pd
import tkinter as tk
import tkinter.messagebox


# TODO: add pack methods!
class PCT:
    def __init__(self):
        print("Init")

    def join_hex(self, data_high, data_low):
        return (data_high << 8) | data_low

    def data_split(self, arr):
        if arr[0] == 0x10:
            if arr[1] == 0x02:
                data_type = "DAT_EEG_WAVE"
                ECG1_wave = self.join_hex(arr[2], arr[3])
                ECG2_wave = self.join_hex(arr[4], arr[5])
                ECG_status = arr[6]
            if arr[1] == 0x03:
                data_type = "DAT_EEG_LEAD"
                lead_info = arr[2]
                overload_warning = arr[3]
            if arr[1] == 0x04:
                data_type = "DAT_EEG_HR"
                heart_rate = self.join_hex(arr[2], arr[3])

        if arr[0] == 0x11:
            if arr[1] == 0x02:
                data_type = "DAT_RESP_WAVE"
                respiration_wave_data1 = arr[2]
                respiration_wave_data2 = arr[3]
                respiration_wave_data3 = arr[4]
                respiration_wave_data4 = arr[5]
                respiration_wave_data5 = arr[6]

            if arr[1] == 0x03:
                data_type = "DAT_RESP_LEAD"
                respiration_rate = self.join_hex(arr[2], arr[3])

        if arr[0] == 0x12:
            if arr[1] == 0x02:
                data_type = "DAT_TEMP_DATA"
                temperature_sensor_status = arr[2]
                temperature_channel1 = self.join_hex(arr[3], arr[4])
                temperature_channel2 = self.join_hex(arr[5], arr[6])

        if arr[0] == 0x13:
            if arr[1] == 0x02:
                data_type = "DAT_SPO2_WAVE"
                o2_wave_data1 = arr[2]
                o2_wave_data2 = arr[3]
                o2_wave_data3 = arr[4]
                o2_wave_data4 = arr[5]
                o2_wave_data5 = arr[6]
                o2_measure_status = arr[7]

            if arr[1] == 0x03:
                data_type = "DAT_SPO2_DATA"
                o2_saturate_info = arr[2]
                pulse_rate = self.join_hex(arr[3], arr[4])
                o2_saturate_data = arr[5]

        if arr[0] == 0x14:
            if arr[1] == 0x02:
                data_type = "DAT_NBP_CUFPRE"
                cuff_pressure = self.join_hex(arr[2], arr[3])
                cuff_type_error = arr[4]
                measure_type = arr[5]

            if arr[1] == 0x03:
                data_type = "DAT_NBP_END"
                measure_type = arr[2]

            if arr[1] == 0x04:
                data_type = "DAT_NBP_RSLT1"
                systolic_pressure = self.join_hex(arr[2], arr[3])
                diastolic_pressure = self.join_hex(arr[4], arr[5])
                mean_artery_pressure = self.join_hex(arr[6], arr[7])

            if arr[1] == 0x05:
                data_type = "DAT_NBP_RSLT2"
                pulse_rate = self.join_hex(arr[2], arr[3])

    def unpack(self, packed):
        check_sum = packed[0]
        data_head = packed[1]
        check_sum += data_head

        i = 1
        while i < 8:
            check_sum += packed[i + 1]
            packed[i] = str((packed[i + 1] & 0x7f) | ((data_head & 0x1) << 7))
            data_head >>= 1
            i += 1

        if (check_sum & 0x7f) != ((packed[9]) & 0x7f):
            return [0, 0, 0, 0, 0, 0, 0, 0]

        return packed[0:8]

    def read_packed_csv(self, data_path):
        try:
            column_names = [
                "module", "datHead", "SecId", "dat1",
                "dat2", "dat3", "dat4", "dat5", "dat6",
                "cal"
            ]
            packed = pd.read_csv(data_path,
                                 names=column_names,
                                 na_values="?", comment='\t',
                                 sep=",", skipinitialspace=True)

            unpacked_column_names = [
                "module", "SecId", "dat1", "dat2",
                "dat3", "dat4", "dat5", "dat6"
            ]
            unpacked = pd.DataFrame(columns=unpacked_column_names)
            ds = []
            count = 0

            for index, row in packed.iterrows():
                row1 = packed.loc[index].values

                ds = self.unpack(row1)
                if (ds == [0, 0, 0, 0, 0, 0, 0, 0]).all():
                    continue

                temp = pd.DataFrame([ds], columns=unpacked_column_names)
                # df = unpacked.append(temp, sort=False)
                unpacked = pd.concat([unpacked, temp], ignore_index=True)
                count += 1

            msg = "Read " + str(count) + " lines."
            tk.messagebox.showinfo('Message', msg)
            return unpacked
        except:
            return [0, 0, 0, 0, 0, 0, 0, 0]

    def read_unpacked_csv(self, data_path):
        try:
            unpacked_column_names = [
                "module", "SecId", "dat1", "dat2",
                "dat3", "dat4", "dat5", "dat6"
            ]
            unpacked = pd.read_csv(data_path,
                                   names=unpacked_column_names,
                                   na_values="?", comment='\t',
                                   sep=",", skipinitialspace=True)

            msg = "Read " + str(len(unpacked)) + " lines."
            tk.messagebox.showinfo('Message', msg)
            return unpacked
        except:
            return [0, 0, 0, 0, 0, 0, 0, 0]


if __name__ == '__main__':
    pct = PCT()
    data_path = "./unpacked.csv"
    hello = pct.read_packed_csv(data_path)

