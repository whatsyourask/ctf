# The Art of Reversing

Platform: HackTheBox

Open exe file in IDA. It specified the file like .NET app. Next, open it in dnSpy to decompile .NET app. Now, we can analyze something like source code of this app.

We need to reverse this words to get a flag `cathhtkeepaln-wymddd`.

```csharp
// Token: 0x0600000A RID: 10 RVA: 0x0000234C File Offset: 0x0000054C
		private void buttonCreateProductKey_Click(object sender, EventArgs e)
		{
			if (this.textBoxUsername.Text.TrimEnd(new char[0]) == "" || this.textBoxDays.Text.TrimEnd(new char[0]) == "")
			{
				MessageBox.Show("Both Username and Number of Days are mandatory!");
				return;
			}
			string text = this.textBoxUsername.Text.TrimEnd(new char[0]);
			int num = Convert.ToInt32(this.textBoxDays.Text);
			this.nToStop = 0;
			this.nCounter = 0;
			this.bContinue = true;
			this.ssOut = "";
			if (text.Length < 3)
			{
				MessageBox.Show("Username must be more than 2 characters!");
				return;
			}
			if (num <= 15 || num > 3650)
			{
				MessageBox.Show("Activation Days must be between 15 and 3650!");
				return;
			}
			this.textBoxProductKey.Text = "";
			Application.DoEvents();
			Cursor.Current = Cursors.WaitCursor;
			int num2 = this.nPr(text.Length, text.Length);
			this.nToStop = num2 / 2;
			char[] word = text.ToCharArray();
			this.GetPer(word);
			string text2 = this.ToR(num);
			text2 = this.DoR(text2);
			Cursor.Current = Cursors.Default;
			this.textBoxProductKey.Text = this.ssOut + "-" + text2;
		}
```

This is a function which will be executed on button click. It does a pretty easy operations. Some validation of user input. More interesting are next functions: `nPr()`, `GetPer()`, `ToR()`, `DoR()`

I used python to reverse operations:

```python
product_key = 'cathhtkeepaln-wymddd'
splited_product_key = product_key.split('-')
word = splited_product_key[0]
text2 = splited_product_key[1]
text2 = text2.upper()
c = '\u0001'
print(text2)
text2 = ''.join([chr(ord(char) - 1) for char in text2])
print(text2)
text2 = text2[::-1]
print(text2)
```

The output is following:

```python
WYMDDD
VXLCCC
CCCLXV
```

Using the last word we can also reverse function ToR to obtain init value:

```csharp
public string ToR(int number)
		{
			if (number < 0 || number > 3999)
			{
				return "";
			}
			if (number < 1)
			{
				return string.Empty;
			}
			if (number >= 1000)
			{
				return "M" + this.ToR(number - 1000);
			}
			if (number >= 900)
			{
				return "CM" + this.ToR(number - 900);
			}
			if (number >= 500)
			{
				return "D" + this.ToR(number - 500);
			}
			if (number >= 400)
			{
				return "CD" + this.ToR(number - 400);
			}
			if (number >= 100)
			{
				return "C" + this.ToR(number - 100);
			}
			if (number >= 90)
			{
				return "XC" + this.ToR(number - 90);
			}
			if (number >= 50)
			{
				return "L" + this.ToR(number - 50);
			}
			if (number >= 40)
			{
				return "XL" + this.ToR(number - 40);
			}
			if (number >= 10)
			{
				return "X" + this.ToR(number - 10);
			}
			if (number >= 9)
			{
				return "IX" + this.ToR(number - 9);
			}
			if (number >= 5)
			{
				return "V" + this.ToR(number - 5);
			}
			if (number >= 4)
			{
				return "IV" + this.ToR(number - 4);
			}
			if (number >= 1)
			{
				return "I" + this.ToR(number - 1);
			}
			return "";
		}
```

It will be the value 365. Next step is to get username of a user. For this task you can try to reverse the following functions:

```csharp
// Token: 0x06000002 RID: 2 RVA: 0x00002070 File Offset: 0x00000270
		private void Do(ref char a, ref char b)
		{
			if (a == b)
			{
				return;
			}
			a ^= b;
			b ^= a;
			a ^= b;
		}

		// Token: 0x06000003 RID: 3 RVA: 0x00002094 File Offset: 0x00000294
		public void GetPer(char[] word)
		{
			int m = word.Length - 1;
			this.GetPer(word, 0, m);
		}

		// Token: 0x06000004 RID: 4 RVA: 0x000020B0 File Offset: 0x000002B0
		private void GetPer(char[] word, int k, int m)
		{
			if (!this.bContinue)
			{
				return;
			}
			if (k == m)
			{
				this.nCounter++;
				if (this.nCounter == this.nToStop)
				{
					this.ssOut = new string(word);
					this.bContinue = false;
					return;
				}
			}
			else
			{
				for (int i = k; i <= m; i++)
				{
					this.Do(ref word[k], ref word[i]);
					this.GetPer(word, k + 1, m);
					this.Do(ref word[k], ref word[i]);
				}
			}
		}
```

The last of them performs permutations, permutations with some rounds in variable nCounter. I didn’t get a thing how to reverse this algorithm. But it has a vulnerability. If you’ll insert `0123456789abc` in the field, you’ll receive the next value `21450c3b6798a`. This value is similar to `cathhtkeepaln`. So, you can compare them and find init value:

```
21450c3b6798a
cathhtkeepaln
0123456789abc
hacktheplanet
```