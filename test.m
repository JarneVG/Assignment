s = tf('s');

m1 = 25; 
m2 = 5;

k1 = 4.1e3;
k2 = 15e3;
c_all = 10:0.01:100;


figure
for index = 1:length(c_all)
    c = c_all(index);
    sys = k2*(c + 2*k1)/((m2*s^2 + c*s + 2*k1 + k2)*(m1*s^2 + 2*k1 + c*s) - (c*s + 2*k1)^2);
    bode(sys);
    hold on
end
hold off