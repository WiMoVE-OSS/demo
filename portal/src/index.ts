import express from "express";
import { engine } from "express-handlebars";
import { exec } from "child_process";
import https from "https";
import {readFileSync} from "fs";

const app = express();
//initialize handlebars
app.engine("handlebars", engine());
app.set("view engine", "handlebars");
app.set("views", "views");

app.use(express.static("static"));

const colors = ["#7a1313", "#037e36", "#1a037e"]


function getVNI(ip: string): number {
  const octets = ip.split(".");
  octets.pop();
  const subnet = octets.pop() ?? "UNKNOWN";
  if(!isNaN(parseInt(subnet))) {
    return (parseInt(subnet) - 1);
  }
  return 0;
}

async function execute(command: string): Promise<string> {
  return new Promise((resolve, reject) => {
    exec(command, function (error, stdout, stderr) {
      resolve(stdout);
    });
  });
}

async function getMAC(ip: string) {
  const potentialMac = await execute(`arp -a ${ip} | cut -d " " -f 4`);
  // check if mac matches regex
  if (potentialMac.match(/([0-9a-f]{2}[:-]){5}([0-9a-f]{2})/g) != null) {
    return potentialMac.trim();
  }
  throw new Error("Unable to find valid MAC");
}

function getColor(vni: number) {
  return colors[vni - 1];
}

async function getAP(mac: string, vni: number) {
  const json = await execute('vtysh -c "show evpn mac vni all json"');
  // const json = await execute(
  //  "cat /home/aarons/Projects/BP/open6ghub/blinkenlights/sample.json"
  //);
  const obj = JSON.parse(json);
  const net = obj[vni.toString()];
  if (!net) {
    console.log("Unkown VNI")
    return "UNKNOWN";
  }
  for (const foundMac of Object.keys(net.macs)) {
    console.log(foundMac)
    console.log(mac)
    console.log("----")
    const dev = net.macs[foundMac];
    if (mac === foundMac && dev.type === "remote") {
      return dev.remoteVtep;
    }
  }
  return "UNKNOWN";
}

function getAPName(apIp: string) {
  if(apIp === "UNKNOWN") {
    return "??"
  }
  const device = apIp.split(".").pop() ?? "0";
  const num = parseInt(device);
  return "AP" + num % 10;
}

app.get("/", async (req, res) => {
  // get clients ip address
  const ip = req.socket.remoteAddress || "";
  const ipv4 = ip.split(":").pop() || "";
  let mac = "UNKNOWN";
  let vni = 0;
  try {
    mac = await getMAC(ipv4);
    vni = getVNI(ipv4)
  } catch (e) {
    console.error(e);
  }
  res.render("home", {
    ip: ipv4,
    vni: vni,
    mac: mac,
    ap: getAPName(await getAP(mac, vni)),
    color: getColor(vni)
  });
});



app.use("/css", express.static("node_modules/water.css/out/"));
app.use("/res", express.static("res/"));

app.all("*", (req, res) => {
  res.redirect("https://demo.vxlan.rocks")
})

app.listen(80, '0.0.0.0', () => {
  console.log("Server started on port 3000");
});

https.createServer({
  key: readFileSync("certs/demo.vxlan.rocks.key", "utf-8"),
  cert: readFileSync("certs/demo.vxlan.rocks.crt", "utf-8"),
}, app).listen(443, '0.0.0.0', () => {
  console.log("Listening on https")
});
