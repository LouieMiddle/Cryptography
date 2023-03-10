%SPN Encryption:
%Inputs
key = [1,1,1,0,0,1,1,1,0,1,1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,1]
plaintext = [0,1,0,0,1,1,1,0,1,0,1,0,0,0,0,1];
sbox = [[0,1,0,0],[0,0,0,1],[1,1,1,0],[1,0,0,0],[1,1,0,1],[0,1,1,0],[0,0,1,0],[1,0,1,1],[1,1,1,1],[1,1,0,0],[1,0,0,1],[0,1,1,1],[0,0,1,1],[1,0,1,0],[0,1,0,1],[0,0,0,0]]
%State initialisation
state = plaintext;
for i=1:4
    %Find the round key
    k =  key(4*i-3:4*i+12)
    %x-or
    state = xor(state,k)
    %Substitutions
    for j=1:4
       input = binvec2dec(fliplr(state(4*(j-1)+1:4*j)))
       state(4*(j-1)+1:4*j) = sbox(4*input+1:4*input+4)
    end
    %Permutation
    if i < 4
        state = [state(1),state(5),state(9),state(13),state(2),state(6),state(10),state(14),state(3),state(7),state(11),state(15),state(4),state(8), state(12),state(16)]
    end
end

i = 5;
%Find the round key
k =  key(4*i-3:4*i+12)
%x-or
ciphertext = xor(state,k)
