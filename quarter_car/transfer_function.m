clear all; close all; clc;

s = tf('s');

% System constants
m1 = 25;
m2 = 5;
k2 = 15000;

% Sweep ranges
k1_vals = linspace(4000, 40000, 20);      % k1 sweep
c_vals  = linspace(1, 10000, 20);         % c sweep

% Frequency range (rad/s)
w_min = 0;
w_max = 62.83;   % = 10 Hz * 2*pi
w = linspace(w_min, w_max, 2000);    % dense sampling

% Storage
I = zeros(length(c_vals), length(k1_vals));

% ---- Double loop over k1 and c ----
for i = 1:length(k1_vals)
    for j = 1:length(c_vals)

        k1 = k1_vals(i);
        c  = c_vals(j);

        % Define transfer function
        teller = k2*(c*s + 2*k1);
        noemer = (m2*s^2 + c*s + 2*k1 + k2)*(m1*s^2 + c*s + 2*k1) ...
                 - (c*s + 2*k1)^2;
        H = teller/noemer;

        % Frequency response |H(jw)|
        Hjw = squeeze(abs(freqresp(H, w)));

        % Numerical integration using trapezoidal rule
        I(j,i) = trapz(w, Hjw);

    end
end

% ---- 3D Surface Plot ----
figure;
surf(k1_vals, c_vals, I, 'EdgeColor', 'none');
xlabel('k1 (N/m)');
ylabel('c (Ns/m)');
zlabel('∫ |H(jω)| dω from 0 to 62.83 rad/s');
title('Integrated Magnitude of Transfer Function vs k1 and c');
colorbar;
grid on;
view(45, 30);

% ---- 2D Plot for smallest k1 ----
k1_min_index = 1;            % index of lowest k1
I_lowest_k = I(:, k1_min_index);

figure;
plot(c_vals, I_lowest_k, 'LineWidth', 2);
xlabel('c (Ns/m)');
ylabel('∫ |H(jω)| dω');
title(['Integrated Response vs c for lowest k1 = ' num2str(k1_vals(1))]);
grid on;
