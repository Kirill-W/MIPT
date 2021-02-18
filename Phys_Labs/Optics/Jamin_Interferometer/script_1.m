%% Calibration plot
T_Calibration = readtable('data_1.xlsx', 'Range', 'B3:C22');

p_C = polyfit(T_Calibration.StripeNumber, T_Calibration.MicrometerPosition_Mm, 1);
f_C = polyval(p_C, T_Calibration.StripeNumber);
err_C = T_Calibration.MicrometerPosition_Mm * 0.004;

errorbar(T_Calibration.StripeNumber, T_Calibration.MicrometerPosition_Mm, err_C, 'k.');
hold on;
plot(T_Calibration.StripeNumber, f_C, '-', 'Color', '#777777');
grid on;

xlabel('Номер полосы m');
ylabel('Положение микрометра z_{m}, мм');
title('Калибровка компенсатора');
str_C = ['z_{m}(m) = (' num2str(round(p_C(1) * 1000) / 1000) '±0,004)m + (' num2str(round(p_C(2) * 100) / 100) '±0,02)'];
legend('Экспериментальные значения', str_C);

%% P(delta_n) plot
T_Pressure = readtable('data_1.xlsx', 'Range', 'E3:F14');

New = (T_Pressure.MicrometerPosition_Mm - p_C(2))/p_C(1) * 6.5*10^(-7);
err_N_y = New .* sqrt((((0.004 + (0.02/15.98))^2)/(T_Pressure.MicrometerPosition_Mm - 15.98).^2 + (0.04/0.2835)^2).^2 ./((T_Pressure.MicrometerPosition_Mm - 15.98)./0.2835)  + (20/65)^2);
err_N_x = ones(size(T_Pressure.Pressure_MmH2O)) * 25;
p_N = polyfit(T_Pressure.Pressure_MmH2O, New, 1);
f_N = polyval(p_N, T_Pressure.Pressure_MmH2O);

errorbar(T_Pressure.Pressure_MmH2O, New, err_N_y(:, 1), err_N_y(:, 1), err_N_x, err_N_x, 'k.');
hold on;
plot(T_Pressure.Pressure_MmH2O, f_N, '-', 'Color', '#777777');
grid on;

xlabel('Давление, мм H_{2}O');
ylabel('δn');
title('Зависимость δn от P для воздуха');
str_N = ['δn = (' num2str(round(p_N(1) * 100000000000) / 100) '±0.16)P*10^{-9} Па^{-1} + (' num2str(round(p_N(2) * 1000000000) / 100) '±0.51)*10^{-7}'];
legend('Расчётные значения', str_N);

%% n (H2O/CO2) plot
T_CO2 = readtable('data_1.xlsx', 'Range', 'H3:I7');

p_CO2 = polyfit(T_CO2.Time_Min, T_CO2.MicrometerPosition_Mm, 1);
f_CO2 = polyval(p_CO2, T_CO2.Time_Min);
err_CO2 = T_CO2.MicrometerPosition_Mm * 0.004;

errorbar(T_CO2.Time_Min, T_CO2.MicrometerPosition_Mm, err_CO2, 'k.');
grid on;
axis([-0.5 7.5 17.12 17.50]);

xlabel('Время, мин.');
ylabel('Положение микрометра z, мм');
title('Изменение показаний микрометра со временем');
legend('Экспериментальные значения');

%%
