main(){
    int x, y, z, a, b, i;
    x = 10;
    y = 20;
    z = x * y;
    
    if (z > 100) {
        a = 5;
        b = 6;
        z = z / a + b;
    };
    
    for (i = 0; i < 10; i = i + 1) {
        x = x + i;
    };
    
    while (y > 0) {
        y = y - 1;
        if (x > y) {
            x = x - 1;
        };
    };
}